import os

from ngl.utils import echo, color
from ngl.client import NotionGameList
from ngl.games.steam import SteamGamesLibrary

# ----------- Variables -----------
# Set token_v2 here
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
STEAM_TOKEN = os.getenv("STEAM_TOKEN")
STEAM_USER = os.getenv("STEAM_USER")
# ---------------------------------

ngl = NotionGameList.login(token_v2=NOTION_TOKEN)
steam = SteamGamesLibrary.login(api_token=STEAM_TOKEN, user_id=STEAM_USER)
