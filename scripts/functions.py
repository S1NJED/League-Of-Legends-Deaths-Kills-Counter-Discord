import json, requests, urllib3, subprocess, os
from requests.exceptions import ConnectionError
from time import sleep
from random import choice

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # Disable warning when verify=False
CWD = os.path.abspath(os.path.dirname(__file__))
MAIN_DIR = os.path.abspath(os.path.join(CWD, ".."))
CONFIG_JSON_ABS_PATH = os.path.join(MAIN_DIR, 'config.json')

DEATHS = "DEATHS"
KILLS  = "KILLS"

def getSummonerName():
    URL = "https://127.0.0.1:2999/liveclientdata/activeplayername"

    while True:
        try:
            req = requests.get(URL, verify=False)
            username = req.json()
            if type(username) is not str:
                continue
            return username
        except ConnectionError:
            print("Cannot get summoner name.") # debug
            return False


def getSummonerScore():
    username = ""
    
    while not username:
        username = getSummonerName()
        sleep(1)
    
    URL = "https://127.0.0.1:2999/liveclientdata/playerscores?summonerName=" + username
    
    while True:
        try:
            req = requests.get(URL, verify=False)
            data = req.json()
            return data   
        except ConnectionError:
            print("Cannot get summoner name.") # debug
            return False


def isGameActive():
    URL = "https://127.0.0.1:2999/liveclientdata/activeplayername" # Any URL /liveclientdata/* would work
    try:
        requests.get(URL, verify=False)
        return True
    except ConnectionError as err:
        return False


def isLeagueClientActive():
    cmd = "tasklist | findstr League" # win10
    res = subprocess.run(cmd, capture_output=True, text=False, shell=True)
    output = res.stdout.strip()
    return True if output else False


def waitForLeagueClient():
    cmd = "tasklist | findstr League"
    
    while True:
        res = subprocess.run(cmd, capture_output=True, text=False, shell=True)
        output = res.stdout.strip()
        if output:
            break
        sleep(1)
    
    print("League client is now active.")
    

def updateCount(eventType, value):
    if not eventType in [DEATHS, KILLS]:
        return print("Event type must be 'DEATHS' or 'KILLS'")

    data = 0
    with open(CONFIG_JSON_ABS_PATH, 'r') as file:
        data = json.load(file)
    
    with open(CONFIG_JSON_ABS_PATH, 'w') as file:
        data[eventType + '_COUNT'] += value
        json.dump(data, file, indent=4)    


def getRandomImages(eventType):
    if not eventType in [DEATHS, KILLS]:
        return print("Event type must be equal to 'DEATHS or 'KILLS'")

    CONFIG = json.loads( open(CONFIG_JSON_ABS_PATH, 'r').read() )
    imageArray = CONFIG[eventType + "_MESSAGE_IMAGES_GIFS_URLS"]
    # If no image/gifs in the config.json then use theses by default
    if not len(imageArray):
        return None
    
    return choice(imageArray)

  
def getGameTime():
    URL = "https://127.0.0.1:2999/liveclientdata/eventdata"
    
    try:
        req = requests.get(URL, verify=False)
        data = req.json()
        seconds = int(data['gameTime']) # seconds gameTime: 300.239293783
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = (seconds % 3600) % 60
        return hours, minutes, seconds
        
    except ConnectionError as err:
        return False


def formatGameTime():
    hours, minutes, seconds = getGameTime()
    time = ""
    if hours:
        time += f"{hours}h "
    if minutes:
        time += f"{minutes} min"
    time += f"{seconds} s"
    return time


def sendDiscordMessage(eventType, currentValue):
    if not eventType in [DEATHS, KILLS]: 
        return print("Event type must be equal to 'DEATHS' or 'KILLS'")
    
    CONFIG = json.loads( open(CONFIG_JSON_ABS_PATH, 'r').read() )
    
    DISCORD_USERNAME = f"<@{CONFIG['DISCORD_USER_ID']}>"
    SUMMONER_USERNAME = getSummonerName()
    WEBHOOK_USERNAME = CONFIG['WEBHOOK']['USERNAME'] or "Lol Death Counter"
    WEBHOOK_AVATAR_URL = CONFIG['WEBHOOK']['AVATAR_URL']
    
    DEATHS_COUNT = CONFIG['DEATHS_COUNT']
    KILLS_COUNT = CONFIG['KILLS_COUNT']
    
    DESCRIPTION = (
        f"{DISCORD_USERNAME} died {currentValue} times in this game.\n"
        f"({DEATHS_COUNT} in total)\n"
        f":hourglass: {formatGameTime()}"
    )
    TITLE = f"{SUMMONER_USERNAME} died ... 💀"
    if eventType == KILLS:
        DESCRIPTION = (
            f"{DISCORD_USERNAME} killed {currentValue} players in this game.\n"
            f"({KILLS_COUNT} in total)\n"
            f":hourglass: {formatGameTime()}"
        )
        TITLE = f"{SUMMONER_USERNAME} killed someone ! ✅"
    
    DISCORD_WEBHOOK_URL = CONFIG['WEBHOOK']['URL']
    HEADERS = {
        "Content-type": "application/json"
    }
    EMBED = {
        "title": TITLE,
        "description": DESCRIPTION,
        "color": CONFIG[eventType + '_COLOR_EMBED'],
        "image": {
            "url": getRandomImages(eventType) # Select random img/gifs from config.json
        }
    }
    PAYLOAD = {
        "username": WEBHOOK_USERNAME,
        "avatar_url": WEBHOOK_AVATAR_URL,
        "embeds": [EMBED]
    }

    req = requests.post(DISCORD_WEBHOOK_URL, headers=HEADERS, json=PAYLOAD)
    status_code = req.status_code

    if status_code != 204:
        with open(os.path.join(MAIN_DIR, 'log.txt'), 'a') as log:
            log.write(str(status_code) + "\n")
        
        print("Cannot send message.")
        return False
    else:
        return True