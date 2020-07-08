from notion.client import NotionClient

from .utils import echo, color


class NotionGameList:

    def __init__(self, token_v2):
        self.client = NotionClient(token_v2=token_v2)

    @classmethod
    def login(cls, token_v2=None):
        # TODO: add log in by email/password
        if token_v2 is None:
            echo(color.y("Log in to Notion: ") + "https://notion.so/login")
            echo("Get 'token_v2' from browser cookies")
            token_v2 = input(color.c("Token: ")).strip()
        return cls(token_v2=token_v2)
