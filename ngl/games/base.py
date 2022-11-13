import typing as tp

from abc import abstractmethod, ABCMeta

TGameID = tp.Union[int, str]  # unique game identifier in library


class GameInfo:

    def __init__(
        self,
        id: TGameID,
        name: str,
        platforms: tp.List[str],
        release_date: tp.Optional[str] = None,
        playtime: tp.Optional[str] = None,
        playtime_minutes: tp.Optional[int] = None,
        logo_uri: tp.Optional[str] = None,
        bg_uri: tp.Optional[str] = None,
        icon_uri: tp.Optional[str] = None,
        free: bool = False
    ):
        self.id = id
        self.name = name
        self.platforms = platforms
        self.release_date = release_date if release_date else None
        self.playtime = playtime if playtime else None
        self.playtime_minutes = playtime_minutes if playtime_minutes else 0
        self.logo_uri = logo_uri if logo_uri else None
        self.bg_uri = bg_uri if bg_uri else None
        self.icon_uri = icon_uri if icon_uri else None
        self.free = free

    def to_dict(self):
        return self.__dict__

class GamesLibrary(metaclass=ABCMeta):

    @abstractmethod
    def get_games_list(self) -> tp.List[TGameID]:
        """ Get game ids from library """
        raise NotImplementedError

    @abstractmethod
    def get_game_info(self, game_id: TGameID) -> GameInfo:
        """ Get game info by id """
        raise NotImplementedError
