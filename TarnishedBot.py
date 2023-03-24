import os
import asyncio
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

async def load():
    for fileName in os.listdir('./Commands'):
        if fileName.endswith('.py'):
            await bot.load_extension(f'Commands.{fileName[:-3]}')

async def main():
    await load()
    await bot.start(botConfig["token"])

asyncio.run(main())

