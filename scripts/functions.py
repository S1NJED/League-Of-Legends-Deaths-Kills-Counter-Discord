import json, requests, urllib3, subprocess, os
from requests.exceptions import ConnectionError
from time import sleep
from random import choice

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # Disable warning when verify=False
CWD = os.path.abspath(os.path.dirname(__file__))
MAIN_DIR = os.path.abspath(os.path.join(CWD, ".."))
CONFIG_JSON_ABS_PATH = os.path.join(MAIN_DIR, 'config.json')


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
    if not eventType in ["DEATHS", "KILLS"]:
        return print("Event type must be 'DEATHS' or 'KILLS'")

    data = 0
    with open(CONFIG_JSON_ABS_PATH, 'r') as file:
        data = json.load(file)
    
    with open(CONFIG_JSON_ABS_PATH, 'w') as file:
        data[eventType + '_COUNT'] += value
        json.dump(data, file, indent=4)    


def getRandomImages(eventType):
    if not eventType in ["DEATHS", "KILLS"]:
        return print("Event type must be equal to 'DEATHS or 'KILLS'")

    CONFIG = json.loads( open(CONFIG_JSON_ABS_PATH, 'r').read() )
    imageArray = CONFIG[eventType + "_MESSAGE_IMAGES_GIFS_URLS"]
    # If no image/gifs in the config.json then use theses by default
    if not len(imageArray):
        if eventType == "DEATHS":
            return "https://media.tenor.com/QgTx6fv4IpAAAAAd/el-risitas-juan-joya-borja.gif"
        elif eventType == "KILLS":
            return "https://tenor.com/view/giga-chad-gif-23143840"
    
    return choice(imageArray)
    

def sendDiscordMessage(eventType):
    if not eventType in ["DEATHS", "KILLS"]: 
        return print("Event type must be equal to 'DEATHS' or 'KILLS'")
    
    CONFIG = json.loads( open(CONFIG_JSON_ABS_PATH, 'r').read() )
    
    DISCORD_USERNAME = f"<@{CONFIG['DISCORD_USER_ID']}>"
    WEBHOOK_USERNAME = CONFIG['WEBHOOK']['USERNAME'] or "Lol Death Counter"
    WEBHOOK_AVATAR_URL = CONFIG['WEBHOOK']['AVATAR_URL'] or "https://cdn.discordapp.com/attachments/775787790923333673/1112419317074628608/IMG_2883.jpg"
    DEATH_COUNT = CONFIG['DEATHS_COUNT']
    KILLS_COUNT = CONFIG['KILLS_COUNT'] # For later ... 
    DESCRIPTION = f"{DISCORD_USERNAME} has died {DEATH_COUNT} times."
    if eventType == "kills": # TODO: later
        DESCRIPTION = f"{DISCORD_USERNAME} killed "
    
    DISCORD_WEBHOOK_URL = CONFIG['WEBHOOK']['URL']
    HEADERS = {
        "Content-type": "application/json"
    }
    EMBED = {
        "title": "RIP" if eventType == "DEATHS" else "✅",
        "description": DESCRIPTION,
        "color": CONFIG['DEATHS_COLOR_EMBED'],
        "image": {
            "url": getRandomImages(eventType)
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