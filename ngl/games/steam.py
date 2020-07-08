import typing as tp
import re

from ngl.api.steam import steamapi
from ngl.utils import echo, color

from .base import GameInfo, GamesLibrary, TGameID


TSteamUserID = tp.Union[str, int]


class SteamGamesLibrary(GamesLibrary):

    def __init__(self, api_token: str, user_id: TSteamUserID):
        self.api = steamapi.core.APIConnection(api_key=api_token, validate_key=True)
        self.user = steamapi.user.SteamUser(user_id) if isinstance(user_id, int) else steamapi.user.SteamUser(userurl=user_id)

    @classmethod
    def login(cls, api_token: tp.Optional[str] = None, user_id: tp.Optional[TSteamUserID] = None):
        # TODO: parse library from profile url ?
        if api_token is None:
            echo(color.y("Get steam token from: ") + "https://steamcommunity.com/dev/apikey")
            api_token = input(color.c("Token: ")).strip()
        if user_id is None:
            echo.y("Pass steam user profile: http://steamcommunity.com/id/<user_id>")
            user_id = input(color.c("User: ")).strip()
            user_id = re.sub(r"^https?:\/\/steamcommunity\.com\/id\/", "", user_id)
        return cls(api_token=api_token, user_id=user_id)

    def get_games_list(self) -> tp.List[TGameID]:
        """ Get game ids from library """

    def get_game_info(self, game_id: TGameID) -> GameInfo:
        """ Get game info by id """
