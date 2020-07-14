import typing as tp
import re
import requests

from ngl.api.steam import steamapi
from ngl.errors import SteamApiError, SteamApiNotFoundError
from ngl.models.steam import SteamStoreApp
from ngl.core import is_valid_link
from ngl.utils import echo, color, lru_cache


from .base import GameInfo, GamesLibrary, TGameID

TSteamUserID = tp.Union[str, int]
TSteamApiKey = str

PLATFORM = "steam"


class SteamStoreApi:
    API_HOST = "https://store.steampowered.com/api/appdetails?appids={}"

    def __init__(self):
        self.session = requests.Session()

    @lru_cache
    def get_game_info(self, app_id: int) -> SteamStoreApp:
        try:
            r = self.session.get(self.API_HOST.format(app_id), timeout=3)
            if not r.ok:
                raise SteamApiError(f"SteamStoreApi error: can't get {r.url}")

            response_body = r.json()[str(app_id)]
            if not response_body["success"]:
                raise SteamApiNotFoundError(f"SteamStoreApi App {app_id} unsuccessfull request")

            return SteamStoreApp(**response_body["data"])

        except SteamApiNotFoundError:
            raise
        except Exception as e:
            raise SteamApiError(error=e)


class SteamGamesLibrary(GamesLibrary):
    IMAGE_HOST = "http://media.steampowered.com/steamcommunity/public/images/apps/"

    def __init__(self, api_key: TSteamApiKey, user_id: TSteamUserID):
        self.api = self._get_api(api_key)
        self.store = SteamStoreApi()
        self.user = self._get_user(user_id)
        self._games = {}

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

    def _image_link(self, app_id: int, img_hash: str):
        return self.IMAGE_HOST + f"{app_id}/{img_hash}.jpg"

    def _get_bg_image(self, app_id: int) -> tp.Optional[str]:
        _bg_img = "https://steamcdn-a.akamaihd.net/steam/apps/{app_id}/{bg}.jpg"
        bg_link = _bg_img.format(app_id=app_id, bg="page.bg")
        if is_valid_link(bg_link):
            return bg_link
        bg_link = _bg_img.format(app_id=app_id, bg="page_bg_generated")
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

    def _fetch_library_games(self):
        if not self._games:
            try:
                for g in self.user.games:
                    steam_game = self.store.get_game_info(g.id)
                    game_logo_uri = steam_game.header_image if steam_game.header_image else self._image_link(g.id, g.img_logo_url)
                    self._games[g.id] = GameInfo(
                        game_id=g.id,
                        game_name=g.name,
                        game_platforms=[PLATFORM],
                        game_release_date=steam_game.release_date,
                        game_playtime=self._playtime_format(g.playtime_forever),
                        game_logo_uri=game_logo_uri,
                        game_bg_uri=self._get_bg_image(g.id),
                        game_icon_uri=self._image_link(g.id, g.img_icon_url),
                        game_free=steam_game.is_free,
                    )
            except Exception as e:
                raise SteamApiError(error=e)

    def get_games_list(self) -> tp.List[TGameID]:
        """ Get game ids from library """
        self._fetch_library_games()
        return list(self._games)

    def get_game_info(self, game_id: TGameID) -> GameInfo:
        """ Get game info by id """
        self._fetch_library_games()

        if game_id not in self._games:
            raise SteamApiError(msg=f"Game with id {game_id} not found")

        return self._games[game_id]
