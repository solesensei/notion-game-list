import typing as tp

from abc import abstractmethod, ABCMeta

TGameID = type("unique game identifier in library")


class GameInfo:

    def __init__(self, game_id: TGameID, game_name: str, game_release_date: str, game_poster_uri: tp.Optional[str] = None):
        self.id = game_id
        self.name = game_name
        self.release_date = game_release_date
        self.poster_uri = game_poster_uri


class GamesLibrary(metaclass=ABCMeta):

    @abstractmethod
    def get_games_list(self) -> tp.List[TGameID]:
        """ Get game ids from library """
        raise NotImplementedError

    @abstractmethod
    def get_game_info(self, game_id: TGameID) -> GameInfo:
        """ Get game info by id """
        raise NotImplementedError
