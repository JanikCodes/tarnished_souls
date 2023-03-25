import os
import asyncio
import discord
from discord.ext import commands
import config
import db

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

async def load():
    for fileName in os.listdir('./Commands'):
        if fileName.endswith('.py'):
            await bot.load_extension(f'Commands.{fileName[:-3]}')

async def main():
    await load()
    await db.init_database()
    await bot.start(config.botConfig["token"])

asyncio.run(main())

