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

echo.g("Logging in Notion...")
ngl = NotionGameList.login(token_v2=NOTION_TOKEN)
echo.g("Logging in Steam...")
steam = SteamGamesLibrary.login(api_key=STEAM_TOKEN, user_id=STEAM_USER)
