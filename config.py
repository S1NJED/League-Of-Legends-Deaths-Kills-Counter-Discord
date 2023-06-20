import json, os

CWD = os.path.dirname(__file__)
CONFIG_JSON_ABS_PATH = os.path.join(CWD, 'config.json')
CONFIG = json.loads( open(CONFIG_JSON_ABS_PATH, 'r').read() )


def confirmChoice(data):
    while True:
        print("Are you sure ? " + data)    
        choice = str(input("y or n > ")).lower()
        if not choice in ["y", "n"]:
            continue
        if choice.lower() == "n":
            return False
        return True

def skip(data):
    if not len(data):
        return True
    return False

print("Press ENTER to skip.\n")

while True:
    msg = "\n1. Enter your League Of Legends executable path (ex: path/to/exe/LeagueClient.exe)\n> "
    LOL_EXECUTABLE_PATH = str(input(msg))
    if skip(LOL_EXECUTABLE_PATH): break
    
    if not LOL_EXECUTABLE_PATH.endswith('LeagueClient.exe'):
        print("Path is invalid, make sure to specify LeagueClient.exe at the end.")
        continue
    
    if not confirmChoice(LOL_EXECUTABLE_PATH):
        continue
    
    CONFIG['LOL_EXECUTABLE_PATH'] = LOL_EXECUTABLE_PATH
    break

while True:
    msg = "\n2. Enter your discord user ID (enable dev mode in settings -> right click on your profile -> copy ID)\n> "
    DISCORD_USER_ID = str(input(msg))
    if skip(DISCORD_USER_ID): break
    
    if len(DISCORD_USER_ID) > 18:
        print("Your discord user ID have to be under 18 characters long.")
        continue
    
    if not confirmChoice(DISCORD_USER_ID):
        continue
    
    CONFIG['DISCORD_USER_ID'] = DISCORD_USER_ID
    break

while True:
    msg = "\n3. Enter a discord webhook URL\n> "
    WEBHOOOK_URL = str(input(msg))
    if skip(WEBHOOOK_URL): break
    
    if not WEBHOOOK_URL.startswith("https://discord.com/api/webhooks/"):
        print("Invalid url.")
        continue
    
    if not confirmChoice(WEBHOOOK_URL):
        continue
    
    CONFIG['WEBHOOK']['URL'] = WEBHOOOK_URL
    break

while True:
    msg = "\n4. Enter a username for your webhook (OPTIONNAL, press enter to skip)\n> "
    WEBHOOK_USERNAME = str(input(msg))
    if skip(WEBHOOK_USERNAME): break
    
    if not confirmChoice(WEBHOOK_USERNAME):
        continue

    CONFIG['WEBHOOK']['USERNAME'] = WEBHOOK_USERNAME
    break

while True:
    msg = "\n5. Enter a image url for your webhook (OPTIONNAL, press Enter to skip)\n> "
    WEBHOOK_AVATAR_URL = str(input(msg))
    if skip(WEBHOOK_AVATAR_URL): break

    if not confirmChoice(WEBHOOK_AVATAR_URL):
        continue
    
    CONFIG['WEBHOOK']['AVATAR_URL'] = WEBHOOK_AVATAR_URL
    break

with open(CONFIG_JSON_ABS_PATH, 'w') as file:
    json.dump(CONFIG, file, indent=4)

print("Configuration done. You can edit manually config.json")
os.system('pause')