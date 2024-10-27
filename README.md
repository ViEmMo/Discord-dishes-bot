# Discord Dishes Bot

![Python Version](https://img.shields.io/badge/python-3.11-blue?style=for-the-badge)

Do you wanna talk? Guess the ingredient! Just a funny bot to make harder join in a Discord voice channel.
Unfortunally, due to my mates language, this bot contains only Italian dishes, but it can be "converted" to a general list of words associated to a main word (eg. Channel name: "creativity" words associated: "innovation", "imagination", "inspiration", "expression", "originality", "vision", "fantasy", "design").

## Table of Contents

1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Set up](#set-up)
5. [Usage](#usage)
6. [Next Features](#next-features)
7. [Contributing](#contributins)

## Features
- **Random recipes** - Get a random recipes and rename a voice channel with the recipe name
- **Kick wrong ingredients** - If the user's nick is not into the recipe ingredients list, kick the user from the voice channel
- **Check every minute** - Check every 60 seconds if the nicks are still corrects ingredients, if not kick users not compliants
- **Hint** - After 3 tries, bot give a hint (eg. word "carrot" in the list --> hint: "ca****") (this feature needs to be improved)

 ## Prerequisites
 - Python 3.11
 - Discord.py library
 - A Discord bot token

 ## Installation
 Clone the repository:
 ```bash
    git clone https://github.com/ViEmMo/Discord-dishes-bot.git
    cd discord-dishes-bot
```

 ## Set up
 Create a .env file in the project root with the following contents:
 ```env
ANNOUNCEMENTS_CHANNEL = HERE THE CHAT ID
VOICE_CHANNEL = HERE THE VOICE CHANNEL ID
KEY = HERE YOUR BOT TOKEN
 ```
 

 ## Usage
 1. Run the bot:
    ```bash
    python ddb.py
    ```
 2. You can change recipe with the command:
    ```bash
    !menu
    ```
## Next Features
- Improve hint system: check if the random ingredients it's already in chat
- !chef command to ask for a hint: re-run rand every time the command is called
- !supermarket command toggle announcements on/off

## Contributing
We welcome contributions! If you have ideas for improvements, bug fixes, or new features, feel free to modify the bot and submit a pull request. 
