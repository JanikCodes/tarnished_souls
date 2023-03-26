import platform
import time
import discord
from discord.ext import commands
import config
import db
from colorama import Back, Fore, Style

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('.'), intents=discord.Intents().all())

        self.cogsList = ["Commands.stats"]

    async def setup_hook(self):
      for ext in self.cogsList:
        await self.load_extension(ext)

    async def on_ready(self):
        prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S UTC", time.gmtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
        print(f"{prfx} Logged in as {Fore.YELLOW + self.user.name}")
        print(f"{prfx} Bot ID {Fore.YELLOW + str(self.user.id)}")
        print(f"{prfx} Discord Version {Fore.YELLOW + discord.__version__}")
        print(f"{prfx} Python Version {Fore.YELLOW + str(platform.python_version())}")
        synced = await self.tree.sync()
        print(f"{prfx} Slash CMDs Synced {Fore.YELLOW + str(len(synced))} Commands")
        await db.init_database()

client = Client()
client.run(config.botConfig["token"])
