import argparse
import os
import sys

from ngl.client import NotionGameList
from ngl.errors import ServiceError
from ngl.games.steam import SteamGamesLibrary
from ngl.utils import echo, color, soft_exit


# ----------- Variables -----------
NOTION_TOKEN = os.getenv("NOTION_TOKEN")  # Notion cookies 'token_v2'
STEAM_TOKEN = os.getenv("STEAM_TOKEN")    # https://steamcommunity.com/dev/apikey
STEAM_USER = os.getenv("STEAM_USER")      # http://steamcommunity.com/id/{STEAM_USER}
DEBUG = os.getenv("DEBUG", "0") == "1"
# ---------------------------------

try:
    parser = argparse.ArgumentParser()
    parser.add_argument("--steam-user", help="Steam user id. http://steamcommunity.com/id/{STEAM_USER}")
    parser.add_argument("--store-bg-cover", help="Use steam store background as a game cover", action="store_true")
    parser.add_argument("--skip-non-steam", help="Do not import games that are no longer on Steam store", action="store_true")
    parser.add_argument("--use-only-library", help="Do not use steam store to fetch game info, fetch everything from library", action="store_true")
    parser.add_argument("--skip-free-steam", help="Do not import free2play games", action="store_true")
    parser.add_argument("--steam-no-cache", help="Do not use cached fetched games", action="store_true")
    args = parser.parse_args()

    assert not (args.skip_non_steam and args.use_only_library), "You can't use --skip-non-steam and --use-only-library together"

    STEAM_USER = args.steam_user or STEAM_USER

    echo.y("Logging into Notion...")
    ngl = NotionGameList.login(token_v2=NOTION_TOKEN)
    echo.g("Logged into Notion!")
    echo.y("Logging into Steam...")
    steam = SteamGamesLibrary.login(api_key=STEAM_TOKEN, user_id=STEAM_USER)
    echo.g("Logged into Steam!")

    echo.y("Getting Steam library games...")
    game_list = sorted(
        [
            steam.get_game_info(id_) for id_ in steam.get_games_list(
                skip_non_steam=args.skip_non_steam,
                skip_free_games=args.skip_free_steam,
                library_only=args.use_only_library,
                no_cache=args.steam_no_cache,
            )
        ], key=lambda x: x.name,
    )
    if not game_list:
        raise ServiceError(msg="no steam games found")

    echo.m(" " * 100 + f"\rGot {len(game_list)} games!")

    echo.y("Creating Notion template page...")
    game_page = ngl.create_game_page()
    echo.g("Created!")
    echo.y("Importing steam library games to Notion...")
    errors = ngl.import_game_list(game_list, game_page, use_bg_as_cover=args.store_bg_cover)
    imported = len(game_list) - len(errors)

    if imported == 0:
        raise ServiceError(msg="no games were imported to Notion")

    if errors:
        echo.r("Not imported games: ")
        for error in sorted(errors, key=lambda x: x.name):
            echo.r(f"- {error.name}")
    echo.g(f"Imported: {imported}/{len(game_list)}\n")

except ServiceError as err:
    echo(err)
    if DEBUG:
        raise err
    soft_exit(1)
except (Exception, KeyboardInterrupt) as err:
    echo(f"\n{err.__class__.__name__}: {err}", file=sys.stderr)
    if DEBUG:
        raise err
    soft_exit(1)

echo.m("Completed!")
soft_exit(0)
