Send a message to discord (via webhooks) when you die or kill someone on League Of Legends 

## About the project

I used the [Riot live client data API](https://developer.riotgames.com/docs/lol#game-client-api_live-client-data-api) to poll data from the current active game.
When you die or kill someone, it send a message to a [Discord](https://discord.com/) server as a embedded message using webhooks.
It shows the all time count and the count during the game.

## Getting started

This program only run on local, and only work for **Windows10** (for the moment) !

### Prerequisites

1. You must have [Python3.X](https://www.python.org/downloads/)

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/S1NJED/League-Of-Legends-Deaths-Kills-Counter-Discord.git
   ```
2. Start a python virtual environment (name it .env)
   ```sh
   python3 -m venv .env
   ```
3. Activate the venv
   ```sh
   .env\Scripts\activate
   ```
4. Install the required packages
   ```sh
   pip install -r requirements.txt
   ```
5. Start config.py and follow the instructions
   ```python
   python3 config.py
   ```
6. You can now deactivate the venv
   ```sh
   deactivate
   ```

## Usage

Once configuration is done, you can now manually start the counter by running:

* `start.py`: start the counter with a console
* `start_background.pyw`: start the counter withount a console

**NB**: *These script launch League Of Legends if not started*

## Roadmap

- [ ] Adding kill counter
- [ ] Create a shortcut to run start.py and league of legends with lol icon 

## Contact

Discord - sinjed
