import platform
import time
import discord
from discord.ext import commands
import config
import db
import logging
from colorama import Back, Fore, Style

class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('.'), intents=discord.Intents().all())

        self.cogsList = ["Commands.stats", "Commands.upgrade_stats"]

    async def setup_hook(self):
      for ext in self.cogsList:
        await self.load_extension(ext)

    async def on_ready(self):
        prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S UTC", time.gmtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
        print(prfx + " Logged in as " + Fore.YELLOW + self.user.name)
        print(prfx + " Bot ID " + Fore.YELLOW + str(self.user.id))
        print(prfx + " Discord Version " + Fore.YELLOW + discord.__version__)
        print(prfx + " Python Version " + Fore.YELLOW + str(platform.python_version()))
        synced = await self.tree.sync()
        print(prfx + " Slash CMDs Synced " + Fore.YELLOW + str(len(synced)) + " Commands")
        await db.init_database()

        logging.warning("Now logging..")



client = Client()
client.run(config.botConfig["token"])