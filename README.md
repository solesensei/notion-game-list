# Notion Game List ![](https://img.shields.io/badge/version-0.0.1-blue)

All your games inside [Notion](https://notion.so).

![notion-x-steam](https://user-images.githubusercontent.com/24857057/87416431-5f8df200-c5d7-11ea-920f-55f06113d388.png)

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
python main.py
```

## Plans

- connect to existing page
- add options for setting status
- add options for importing specific games
- load game covers with better resolution (game DB, steamstore?)
- options for disabling/enabling icons
- parse recent games
- login to notion with password
