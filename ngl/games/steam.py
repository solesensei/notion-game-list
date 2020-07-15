import re
import typing as tp

import requests

from ngl.api.steam import steamapi
from ngl.core import is_valid_link
from ngl.errors import SteamApiError, SteamApiNotFoundError, SteamStoreApiError
from ngl.models.steam import SteamStoreApp
from ngl.utils import color, echo, retry, dump_to_file, load_from_file

from .base import GameInfo, GamesLibrary, TGameID


TSteamUserID = tp.Union[str, int]
TSteamApiKey = str

PLATFORM = "steam"


class SteamStoreApi:
    API_HOST = "https://store.steampowered.com/api/appdetails?appids={}"

    def __init__(self):
        self.session = requests.Session()
        self._cache = {}

    @retry(SteamStoreApiError, retry_num=1, initial_wait=30, backoff=1, raise_on_error=False, debug_msg="Limit StoreSteamAPI requests exceeded", debug=True)
    def get_game_info(self, game_id: TGameID) -> tp.Optional[SteamStoreApp]:
        game_id = str(game_id)
        if game_id in self._cache:
            return self._cache[game_id]
        try:
            r = self.session.get(self.API_HOST.format(game_id), timeout=3)
            if not r.ok:
                raise SteamStoreApiError(f"can't get {r.url}, code: {r.status_code}, text: {r.text}")

            response_body = r.json()[str(game_id)]
            if not response_body["success"]:
                raise SteamApiNotFoundError(f"Game {game_id} unsuccessfull request")

            self._cache[game_id] = SteamStoreApp(**response_body["data"])
            return self._cache[game_id]
        except (SteamApiNotFoundError, SteamStoreApiError):
            raise
        except Exception as e:
            raise SteamApiError(error=e)


class SteamGamesLibrary(GamesLibrary):
    IMAGE_HOST = "http://media.steampowered.com/steamcommunity/public/images/apps/"
    CACHE_GAME_FILE = "game_info_cache.json"

    def __init__(self, api_key: TSteamApiKey, user_id: TSteamUserID):
        self.api = self._get_api(api_key)
        self.store = SteamStoreApi()
        self.user = self._get_user(user_id)
        self._games = {}
        self._store_skipped = []

    def _get_api(self, api_key: TSteamApiKey):
        try:
            return steamapi.core.APIConnection(api_key=api_key, validate_key=True)
        except Exception as e:
            raise SteamApiError(error=e)

    def _get_user(self, user_id: TSteamUserID):
        try:
            return steamapi.user.SteamUser(user_id) if isinstance(user_id, int) else steamapi.user.SteamUser(userurl=user_id)
        except steamapi.errors.UserNotFoundError:
            raise SteamApiError(msg=f"User {user_id} not found")
        except Exception as e:
            raise SteamApiError(error=e)

    @classmethod
    def login(cls, api_key: tp.Optional[TSteamApiKey] = None, user_id: tp.Optional[TSteamUserID] = None):
        # TODO: parse library from profile url ?
        if api_key is None:
            echo(color.y("Get steam token from: ") + "https://steamcommunity.com/dev/apikey")
            api_key = input(color.c("Token: ")).strip()
        if user_id is None:
            echo.y("Pass steam user profile id.")
            user_id = input(color.c("User: http://steamcommunity.com/id/")).strip()
            user_id = re.sub(r"^https?:\/\/steamcommunity\.com\/id\/", "", user_id)
        return cls(api_key=api_key, user_id=user_id)

    def _image_link(self, game_id: TGameID, img_hash: str):
        return self.IMAGE_HOST + f"{game_id}/{img_hash}.jpg"

    def _get_bg_image(self, game_id: TGameID) -> tp.Optional[str]:
        _bg_img = "https://steamcdn-a.akamaihd.net/steam/apps/{game_id}/{bg}.jpg"
        bg_link = _bg_img.format(game_id=game_id, bg="page.bg")
        if is_valid_link(bg_link):
            return bg_link
        bg_link = _bg_img.format(game_id=game_id, bg="page_bg_generated")
        if is_valid_link(bg_link):
            return bg_link
        return None

    @staticmethod
    def _playtime_format(playtime_in_minutes):
        if playtime_in_minutes == 0:
            return "never"
        if playtime_in_minutes < 120:
            return f"{playtime_in_minutes} minutes"
        return f"{playtime_in_minutes // 60} hours"

    def _cache_game(self, game_info: GameInfo):
        g = load_from_file(self.CACHE_GAME_FILE)
        g[str(game_info.id)] = game_info.to_dict()
        dump_to_file(g, self.CACHE_GAME_FILE)

    def _load_cached_games(self, skip_free_games: bool=False):
        g = load_from_file(self.CACHE_GAME_FILE)
        for id_, game_dict in g.items():
            game_info = GameInfo(**game_dict)
            if skip_free_games and game_info.free:
                continue
            self._games[id_] = game_info

    def _fetch_library_games(self, skip_non_steam: bool = False, skip_free_games: bool = False, no_cache: bool = False, force: bool = False):
        if force or not self._games:
            if not no_cache:
                self._load_cached_games(skip_free_games=skip_free_games)
            try:
                number_of_games = len(self.user.games)
                for i, g in enumerate(self.user.games):
                    game_id = str(g.id)
                    if game_id in self._games:
                        continue
                    echo.c(" " * 100 + f"\rFetching [{i}/{number_of_games}]: {g.name}", end="\r")
                    try:
                        steam_game = self.store.get_game_info(game_id)
                        if steam_game is None:
                            echo.m(f"Game {g.name} id:{game_id} not fetched from Steam store, skip it!")
                            self._store_skipped.append(game_id)
                    except SteamApiNotFoundError:
                        if skip_non_steam:
                            echo.m(f"Game {g.name} id:{game_id} not found in Steam store, skip it")
                            continue
                        echo.r(f"Game {g.name} id:{game_id} not found in Steam store, fetching details from library")
                        steam_game = None

                    logo_uri = steam_game.header_image if steam_game is not None and steam_game.header_image else self._image_link(game_id, g.img_logo_url)
                    game_info = GameInfo(
                        id=game_id,
                        name=g.name,
                        platforms=[PLATFORM],
                        release_date=steam_game.release_date if steam_game is not None else None,
                        playtime=self._playtime_format(g.playtime_forever),
                        logo_uri=logo_uri,
                        bg_uri=self._get_bg_image(game_id),
                        icon_uri=self._image_link(game_id, g.img_icon_url),
                        free=steam_game.is_free if steam_game is not None else None,
                    )
                    if steam_game is not None:
                        self._cache_game(game_info)
                    if skip_free_games and game_info.free:
                        continue
                    self._games[game_id] = game_info
            except Exception as e:
                raise SteamApiError(error=e)

    def get_games_list(self, **kwargs) -> tp.List[TGameID]:
        """ Get game ids from library """
        self._fetch_library_games(**kwargs)
        return list(self._games)

    def get_game_info(self, game_id: TGameID, **kwargs) -> GameInfo:
        """ Get game info by id """
        self._fetch_library_games(**kwargs)

        if game_id not in self._games:
            raise SteamApiError(msg=f"Game with id {game_id} not found")

        return self._games[game_id]
