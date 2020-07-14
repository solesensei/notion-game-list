import os
import sys

from ngl.client import NotionGameList
from ngl.errors import ServiceError
from ngl.games.steam import SteamGamesLibrary
from ngl.utils import echo

# ----------- Variables -----------
NOTION_TOKEN = os.getenv("NOTION_TOKEN")  # Notion cookies 'token_v2'
STEAM_TOKEN = os.getenv("STEAM_TOKEN")    # https://steamcommunity.com/dev/apikey
STEAM_USER = os.getenv("STEAM_USER")      # http://steamcommunity.com/id/{STEAM_USER}
# ---------------------------------

try:
    echo.y("Logging into Notion...")
    ngl = NotionGameList.login(token_v2=NOTION_TOKEN)
    echo.g("Logged into Notion!")
    echo.y("Logging into Steam...")
    steam = SteamGamesLibrary.login(api_key=STEAM_TOKEN, user_id=STEAM_USER)
    echo.g("Logged into Steam!")

    echo.y("Getting Steam library games...")
    game_list = [steam.get_game_info(id_) for id_ in steam.get_games_list()]
    if not game_list:
        raise ServiceError(msg="no steam games found")

    echo.m(f"Got {len(game_list)} games!")

    echo.y("Creating Notion template page...")
    game_page = ngl.create_game_page()
    echo.g("Created!")
    echo.y("Importing steam library games to Notion...")
    errors = ngl.import_game_list(game_list, game_page)
    imported = len(game_list) - len(errors)

    if imported == 0:
        raise ServiceError(msg="no games were imported to Notion")

    if errors:
        echo.r("Not imported games: ")
        for e in sorted(errors, key=lambda x: x.name):
            echo.r(f"- {e.name}")
    echo.g(f"\nImported: {imported}/{len(game_list)}\n")

except ServiceError as e:
    echo(e)
    sys.exit(1)

echo.m("Completed!")
