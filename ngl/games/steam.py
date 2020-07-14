import typing as tp
import re

from ngl.api.steam import steamapi
from ngl.errors import SteamApiError
from ngl.utils import echo, color

from .base import GameInfo, GamesLibrary, TGameID

TSteamUserID = tp.Union[str, int]
TSteamApiKey = str

PLATFORM = "steam"


class SteamGamesLibrary(GamesLibrary):
    IMAGE_HOST = "http://media.steampowered.com/steamcommunity/public/images/apps/"

    def __init__(self, api_key: TSteamApiKey, user_id: TSteamUserID):
        self.api = self._get_api(api_key)
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
                self._games = {
                    g.id: GameInfo(
                        game_id=g.id,
                        game_name=g.name,
                        game_platforms=[PLATFORM],
                        game_playtime=self._playtime_format(g.playtime_forever),
                        game_logo_uri=self._image_link(g.id, g.img_logo_url),
                        game_icon_uri=self._image_link(g.id, g.img_icon_url),
                    )
                    for g in self.user.games
                }
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
