from notion.block import CollectionViewPageBlock
from notion.client import NotionClient
from notion.operations import build_operation

from .utils import echo, color


class NotionGameList:

    def __init__(self, token_v2):
        self.client = NotionClient(token_v2=token_v2)
        self._icon = "👾"

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
        v = page.children.add_new(CollectionViewPageBlock)
        v.collection = self.client.get_collection(self.client.create_record("collection", parent=v, schema=self._game_list_schema()))
        v.title = title
        v.description = description
        view = v.views.add_new(view_type="table")
        with self.client.as_atomic_transaction():
            self.client.submit_transaction(
                build_operation(view.id, path=[], command="update", args=self._properites_format(), table="collection_view")
            )
        with self.client.as_atomic_transaction():
            self.client.submit_transaction(
                build_operation(v.collection.id, path=["icon"], command="set", args=self._icon, table="collection")
            )
        return v

    def connect_page(self, url):
        pass

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
                    }
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
                        "color": "red",
                        "value": "Switch",
                    },
                    {
                        "color": "blue",
                        "value": "PS4",
                    },
                ],
            },
            "notes": {"name": "Notes", "type": "text"},
            "time": {"name": "Time", "type": "date"},
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
                        "property": "notes",
                        "visible": True,
                        "width": 200
                    }
                ]
            }
        }
