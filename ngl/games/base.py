import typing as tp

from abc import abstractmethod, ABCMeta

TGameID = tp.Union[int, str]  # unique game identifier in library


class GameInfo:

    def __init__(
        self,
        game_id: TGameID,
        game_name: str,
        game_release_date: tp.Optional[str] = None,
        game_playtime: tp.Optional[str] = None,
        game_logo_uri: tp.Optional[str] = None,
        game_icon_uri: tp.Optional[str] = None,
    ):
        self.id = game_id
        self.name = game_name
        self.release_date = game_release_date
        self.playtime = game_playtime
        self.logo_uri = game_logo_uri
        self.icon_uri = game_icon_uri


class GamesLibrary(metaclass=ABCMeta):

    @abstractmethod
    def get_games_list(self) -> tp.List[TGameID]:
        """ Get game ids from library """
        raise NotImplementedError

    @abstractmethod
    def get_game_info(self, game_id: TGameID) -> GameInfo:
        """ Get game info by id """
        raise NotImplementedError
