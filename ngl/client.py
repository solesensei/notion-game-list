import typing as tp
from datetime import datetime

from notion.block import CollectionViewPageBlock, DividerBlock, CalloutBlock
from notion.client import NotionClient
from notion.collection import Collection, CollectionRowBlock
from notion.operations import build_operation

from ngl.errors import ServiceError
from ngl.games.base import GameInfo

from .utils import echo, color


class NotionGameList:
    PAGE_COVER = "https://images.unsplash.com/photo-1559984430-c12e199879b6?ixlib=rb-1.2.1&q=85&fm=jpg&crop=entropy&cs=srgb&ixid=eyJhcHBfaWQiOjYzOTIxfQ"
    PAGE_ICON = "🎮"

    def __init__(self, token_v2):
        self.client = NotionClient(token_v2=token_v2)
        self._gl_icon = "👾"

    @classmethod
    def login(cls, token_v2=None):
        # TODO: add log in by email/password
        if token_v2 is None:
            echo(color.y("Log in to Notion: ") + "https://notion.so/login")
            echo("Get 'token_v2' from browser cookies")
            token_v2 = input(color.c("Token: ")).strip()
        return cls(token_v2=token_v2)

    def create_game_page(self, title: str = "Notion Game List", description: str = "My game list"):
        page = self.client.current_space.add_page(title + " [generated]")
        callout = page.children.add_new(CalloutBlock)
        callout.title = "All your games inside Notion\n\n**Github:** [https://github.com/solesensei/notion-game-list](https://github.com/solesensei/notion-game-list)"
        page.children.add_new(DividerBlock)
        v = page.children.add_new(CollectionViewPageBlock)
        v.collection = self.client.get_collection(self.client.create_record("collection", parent=v, schema=self._game_list_schema()))
        v.title = title
        v.description = description
        table = v.views.add_new(view_type="table")
        gallery = v.views.add_new(view_type="gallery")
        calendar = v.views.add_new(view_type="calendar")
        board = v.views.add_new(view_type="board")
        table.name = "List"
        gallery.name = "Gallery"
        calendar.name = "Calendar"
        board.name = "Board"
        with self.client.as_atomic_transaction():
            # Main Page: callout icon 💡
            self.client.submit_transaction(
                build_operation(callout.id, path=["format", "page_icon"], command="set", args="💡", table="block")
            )
            # Main Page: callout background
            self.client.submit_transaction(
                build_operation(callout.id, path=["format"], command="update", args=dict(block_color="brown_background"), table="block")
            )
            # Main Page: set cover image
            self.client.submit_transaction(
                build_operation(page.id, path=["format", "page_cover"], command="set", args=self.PAGE_COVER, table="block")
            )
            # Main Page: set icon 🎮
            self.client.submit_transaction(
                build_operation(page.id, path=["format", "page_icon"], command="set", args=self.PAGE_ICON, table="block")
            )
        with self.client.as_atomic_transaction():
            # Game List Page: set icon 👾
            self.client.submit_transaction(
                build_operation(v.collection.id, path=["icon"], command="set", args=self._gl_icon, table="collection")
            )
            # Table: format columns
            self.client.submit_transaction(
                build_operation(table.id, path=[], command="update", args=self._properites_format(), table="collection_view")
            )
            # Board: group by status
            self.client.submit_transaction(
                build_operation(board.id, path=[], command="update", args=dict(query2={"group_by": "status"}), table="collection_view")
            )
            # Gallery: cover image
            self.client.submit_transaction(
                build_operation(gallery.id, path=[], command="update", args=self._gallery_format(), table="collection_view")
            )
        return v

    def connect_page(self, url):
        pass

    def _add_row(self, collection: Collection, **row_data) -> CollectionRowBlock:
        return collection.add_row(**row_data)

    @staticmethod
    def _parse_date(date_str: tp.Optional[str]):
        if not date_str:
            return None
        check_date_formats = (r"%d %b, %Y", r"%b %d, %Y", r"%b %Y", r"%d %b %Y", r"%b %d %Y", r"%Y")
        for fmt in check_date_formats:
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                pass
        echo.r("\nDate: '{}' does not match any of formats '{}' | skip".format(date_str, "', '".join(check_date_formats)))
        return None

    def add_game(self, game: GameInfo, game_page: CollectionViewPageBlock, use_bg_as_cover: bool = False) -> bool:
        row_data = {"title": game.name, "platforms": game.platforms, "release_date": self._parse_date(game.release_date), "notes": f"Playtime: {game.playtime}"}
        row = self._add_row(game_page.collection, **row_data)
        row.icon = game.icon_uri or self._gl_icon
        with self.client.as_atomic_transaction():
            # Game cover image
            cover_img_uri = game.bg_uri or game.logo_uri if use_bg_as_cover else game.logo_uri
            if cover_img_uri:
                self.client.submit_transaction(
                    build_operation(row.id, path=["format", "page_cover"], command="set", args=cover_img_uri, table="block")
                )
            else:
                echo.y(f"Game '{game.name}:{game.id}' does not have cover image")
        return True

    def import_game_list(self, game_list: tp.List[GameInfo], game_page: CollectionViewPageBlock, **kwargs) -> tp.List[GameInfo]:
        errors = []
        for i, game in enumerate(game_list, start=1):
            echo.c(f"Imported: {i}/{len(game_list)}", end="\r")
            if not self.add_game(game, game_page, **kwargs):
                errors.append(game)
        return errors

    @staticmethod
    def _gallery_format():
        return {
            "format": {
                "gallery_cover": {
                    "type": "page_cover"
                },
                "gallery_properties": [
                    {
                        "property": "title",
                        "visible": True
                    },
                    {
                        "property": "notes",
                        "visible": False
                    },
                    {
                        "property": "platforms",
                        "visible": True
                    },
                    {
                        "property": "score",
                        "visible": False
                    },
                    {
                        "property": "status",
                        "visible": True
                    },
                    {
                        "property": "time",
                        "visible": False
                    }
                ]
            }
        }

    @staticmethod
    def _game_list_schema():
        return {
            "title": {"name": "Title", "type": "title"},
            "status": {
                "name": "Status",
                "type": "select",
                "options": [
                    {
                        "color": "green",
                        "value": "Completed"
                    },
                    {
                        "color": "yellow",
                        "value": "Playing"
                    },
                    {
                        "color": "blue",
                        "value": "Planned"
                    },
                    {
                        "color": "gray",
                        "value": "Stalled"
                    },
                    {
                        "color": "red",
                        "value": "Dropped"
                    },
                ]
            },
            "score": {
                "name": "Score",
                "type": "select",
                "options": [
                    {
                        "color": "green",
                        "value": "10",
                    },
                    {
                        "color": "orange",
                        "value": "9",
                    },
                    {
                        "color": "yellow",
                        "value": "8",
                    },
                    {
                        "color": "blue",
                        "value": "7",
                    },
                    {
                        "color": "purple",
                        "value": "6",
                    },
                    {
                        "color": "brown",
                        "value": "5",
                    },
                    {
                        "color": "pink",
                        "value": "4",
                    },
                    {
                        "color": "orange",
                        "value": "3",
                    },
                    {
                        "color": "gray",
                        "value": "2",
                    },
                    {
                        "color": "red",
                        "value": "1",
                    }
                ],
            },
            "platforms": {
                "name": "Platforms",
                "type": "multi_select",
                "options": [
                    {
                        "color": "gray",
                        "value": "Steam",
                    },
                    {
                        "color": "default",
                        "value": "PC",
                    },
                    {
                        "color": "red",
                        "value": "Switch",
                    },
                    {
                        "color": "blue",
                        "value": "PlayStation",
                    },
                    {
                        "color": "green",
                        "value": "Xbox",
                    },
                ],
            },
            "notes": {"name": "Notes", "type": "text"},
            "time": {"name": "Time", "type": "date"},
            "release_date": {"name": "Release Date", "type": "date"},
        }

    @staticmethod
    def _properites_format():
        return {
            "format": {
                "table_properties": [
                    {
                        "property": "title",
                        "visible": True,
                        "width": 280
                    },
                    {
                        "property": "status",
                        "visible": True,
                        "width": 100
                    },
                    {
                        "property": "score",
                        "visible": True,
                        "width": 100
                    },
                    {
                        "property": "platforms",
                        "visible": True,
                        "width": 200
                    },
                    {
                        "property": "time",
                        "visible": True,
                        "width": 200
                    },
                    {
                        "property": "release_date",
                        "visible": True,
                        "width": 200
                    },
                    {
                        "property": "notes",
                        "visible": True,
                        "width": 200
                    }
                ]
            }
        }
