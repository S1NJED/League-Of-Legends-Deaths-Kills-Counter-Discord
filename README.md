Send a message to discord (via webhooks) when you die or kill someone on League Of Legends 

![example_message](https://cdn.discordapp.com/attachments/1008888960895963206/1120839755819655270/image.png)

## About the project

I used the [Riot live client data API](https://developer.riotgames.com/docs/lol#game-client-api_live-client-data-api) to poll data from the current active game.
When you *die* or *kill* someone, it send a embedded message to a [Discord](https://discord.com/) server using discord webhooks.
It shows the all time count and the count during the game.

## Getting started

This program only run in local, and only work for **Windows10** (for the moment) !

### Prerequisites

1. You must have [Python3.X](https://www.python.org/downloads/)

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/S1NJED/League-Of-Legends-Deaths-Kills-Counter-Discord.git
   ```
2. Change the Current Working Directory
   ```sh
   cd League-Of-Legends-Deaths-Kills-Counter-Discord
   ```
3. Start the setup.bat file or double click on it
   ```sh
   setup.bat
   ```

## Usage

Once the configuration is done, you can now manually start the counter by running:

* `start.py`: start the counter with a console
* `start_background.pyw`: start the counter without console

**NB**: *Theses scripts launch League Of Legends if it is not running*

## Roadmap

- [ ] Adding kill counter
- [ ] Create a shortcut to run start.py and league of legends with lol icon 

## Contact

Discord - sinjed