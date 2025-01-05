# Notion Game List ![](https://img.shields.io/badge/version-0.1.1-blue) ![](https://app.travis-ci.com/solesensei/notion-game-list.svg?branch=master) [![discuss](https://img.shields.io/reddit/subreddit-subscribers/notion?label=Discuss%20r%2Fnotion-games-list&style=social)](https://www.reddit.com/r/Notion/comments/jiy1sb/notion_games_list/?utm_source=share&utm_medium=web2x&context=3) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) <a href="https://www.buymeacoffee.com/solesensei"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" height="20px"></a>


All your games inside [Notion](https://www.notion.so/solesensei/Notion-Game-List-generated-0d0d39993755415bb8812563a2781d84).

![notion-x-steam](https://user-images.githubusercontent.com/24857057/87418150-eb088280-c5d9-11ea-87b1-ab77979a1b25.png)

## Requirements

Python 3.6+

```bash
# Clone with submodules
git clone --recurse-submodules git@github.com:solesensei/notion-game-list.git

# Create virtual environment
python -m venv notion-game-list-venv && source notion-game-list-venv/bin/activate

# Install requirements
pip install -r requirements.txt -U
```

## How it works

The tool uses 2 Web API clients for Steam and Notion.  

### Steam

I used [Web SteamAPI client](https://github.com/smiley/steamapi) written by [@smiley](https://github.com/smiley).

**Authentification:**
- [Get APIKey](https://steamcommunity.com/dev/apikey)
- Add to environment variable `STEAM_TOKEN` (optional)
- Add your `steamcommunity.com/id/{user_id}` to `STEAM_USER` (optional)

### Notion

For notion i used [notion-py client](https://github.com/jamalex/notion-py) written by [@jamalex](https://github.com/jamalex).

**Authentification:**

- Login to [notion.so](https://notion.so) with your regular email and password
- Open browser cookies and copy `token_v2`
<img src="https://user-images.githubusercontent.com/24857057/87415393-b4c90400-c5d5-11ea-9f67-79983a95bce9.png" alt="click to open" width="300">

- Pass `token_v2` to system environment variable `NOTION_TOKEN` (optional)

## Usage

Check [releases](https://github.com/solesensei/notion-game-list/releases/latest) and get binary tool for os you run, or you can use pure python.

```bash
python main.py -h  # help

python main.py --steam-user solesensei  # run for steam user_id = solesensei

python main.py --store-bg-cover --skip-non-steam  # use store steam background as cover and skip games that are no longer in store

python main.py --skip-free-steam  # import all games except of free2play

python main.py --steam-no-cache  # do not use game_info_cache.json, you can also remove the file
```

[![notion-example](https://user-images.githubusercontent.com/24857057/87416955-21450280-c5d8-11ea-976e-3242bc61ec49.png)](https://www.notion.so/solesensei/Notion-Game-List-generated-0d0d39993755415bb8812563a2781d84)

_[result here](https://www.notion.so/solesensei/Notion-Game-List-generated-0d0d39993755415bb8812563a2781d84)_

_feel free to contribute and create issues_

<a href="https://www.buymeacoffee.com/solesensei" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

## Plans

- rewrite on official [notion api](https://developers.notion.com/)
- connect to existing page
- update existing page values, do not recreate databases
- add options for setting status
- add options for importing specific games
- options for disabling/enabling icons
- parse recent games
- login to notion with password
- add proxy for unlimited requests to Steam Store Web Api (limit: 200 games per 5 minutes)
- ~add release date~ done in v0.0.3
- ~load game covers with better resolution (game DB, steamstore?)~ done in v0.0.2
