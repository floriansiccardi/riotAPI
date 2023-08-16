# League of Legends summoner stats

This open source code, coding in Python with Riot developper API, allow you to access to your match history datas.

### Requirements :
  - API key : freely available on https://developer.riotgames.com/ official Riot website. Need to be updated every 24h.
  - Python 3.9 (or newer) and basics librairies (numpy, pandas, os, time, json, matplotlib).
  - A summoner name and region associated.

### How to use :
  - Edit main.py
  - Enter you API key, need to be updated every 24h.
  - Enter your Summoner name (in game name) and your region (this version offer NA, EUW, EUN, KR and OC regions).
  - Choose the categories you want to rank (this version offer Kill, Death, Assist, KD, Damage (damage dealt), Tank (damage taken), Golds).
  - Run main.py

### Additionnals notes :
  - A program security allow you to exceed your API requests limit (20 per second or 100 per 2 minutes).
  - Every match is saved on your local folder, to reuse them for others stats.

