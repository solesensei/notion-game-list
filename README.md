# Notion Game List ![](https://img.shields.io/badge/version-0.0.2-blue)

All your games inside [Notion](https://notion.so).

![notion-x-steam](https://user-images.githubusercontent.com/24857057/87418150-eb088280-c5d9-11ea-87b1-ab77979a1b25.png)

## Requirements

Python 3.6+

```bash
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

```bash
python main.py -h
```

![notion-example](https://user-images.githubusercontent.com/24857057/87416955-21450280-c5d8-11ea-976e-3242bc61ec49.png)

## Plans

- connect to existing page
- add options for setting status
- add options for importing specific games
- ~load game covers with better resolution (game DB, steamstore?)~ done in v0.0.2
- options for disabling/enabling icons
- parse recent games
- login to notion with password
