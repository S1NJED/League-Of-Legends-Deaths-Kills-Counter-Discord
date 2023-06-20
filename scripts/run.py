import json, os
from functions import isLeagueClientActive
from main import main

CWD = os.path.dirname(__file__)
MAIN_DIR = os.path.abspath(os.path.join(CWD, ".."))
CONFIG_JSON_ABS_PATH = os.path.join(MAIN_DIR, 'config.json')

CONFIG = json.loads( open(CONFIG_JSON_ABS_PATH, 'r').read() )

# Start League Of Legends
if not isLeagueClientActive():
    LOL_EXECUTABLE_PATH = CONFIG['LOL_EXECUTABLE_PATH']
    if not LOL_EXECUTABLE_PATH:
        print("LOL_EXECUTABLE_PATH is not defined in config.json")
        os.system('pause')
        raise ValueError
    os.startfile( LOL_EXECUTABLE_PATH )

# Start the main.py file
main()

os.system('exit')