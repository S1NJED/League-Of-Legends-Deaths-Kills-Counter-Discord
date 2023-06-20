import os
from functions import *
from time import sleep

DEATHS = "DEATHS"
KILLS  = "KILLS"

def main():
    
    # Wait for league client to start if not active
    if not isLeagueClientActive():
        waitForLeagueClient()

    print("Death counter is starting...")

    # TODO: kill count for later ...
    while isLeagueClientActive():
        previousKillsCount  = 0
        previousDeathsCount = 0
        
        while isGameActive():
            data = getSummonerScore()
            currentKillsCount = data['kills']
            currentDeathsCount = data['deaths']

            if previousDeathsCount != currentDeathsCount:
                print("You died.")
                updateCount(DEATHS, (currentDeathsCount - previousDeathsCount))
                sendDiscordMessage(DEATHS)
                previousDeathsCount = currentDeathsCount

            sleep(3)

    print("League Client is no longer active, exit.")
    os.system('exit')