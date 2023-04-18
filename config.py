# import json
import os

botConfig = None

# load bot token from json
# with open('bot.json') as file:
#     botConfig = json.load(file)

# load bot token from env var
botConfig = os.getenv("BOTTOKEN")