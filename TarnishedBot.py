import discord
from discord.ext import commands
import json
import mysql.connector
import database

#load bot token from json
with open('bot.json') as file:
    botConfig = json.load(file)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
result = database.Get_Users()
print(result)

bot.run(botConfig["token"])


