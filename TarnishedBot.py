import logging
import os
import platform
import time
import traceback
import config
import discord
from colorama import Back, Fore, Style
from discord.ext import commands, tasks
import db

MY_GUILD = discord.Object(id=config.botConfig["hub-server-guild-id"])
UPDATE_ITEMS = False
FILL_FIRST_TIME_DATA = False

class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!-&%', intents=discord.Intents().all())
    async def setup_hook(self):
        for fileName in os.listdir('./Commands'):
            if fileName.endswith('.py'):
                await self.load_extension(f'Commands.{fileName[:-3]}')

        await self.tree.sync()

    async def on_ready(self):
        prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S UTC",
                                                        time.gmtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
        print(f"{prfx} Logged in as {Fore.YELLOW} {self.user.name}")
        print(f"{prfx} Bot ID {Fore.YELLOW} {str(self.user.id)}")
        print(f"{prfx} Discord Version {Fore.YELLOW} {discord.__version__}")
        print(f"{prfx} Python Version {Fore.YELLOW} {str(platform.python_version())}")
        print(f"{prfx} Bot Version 0.1")
        await db.init_database()

        logging.warning("Now logging..")

        if UPDATE_ITEMS:
            db.fill_db_weapons()
            print("Added weapon data..")
            db.fill_db_armor()
            print("Added armor data..")

        if FILL_FIRST_TIME_DATA:
            db.fill_db_init()
            print("Added init data..")

        self.printer.start()

    @tasks.loop(hours=12)
    async def printer(self):
        await db.update_usernames(self)

    async def send_error_message(self, error):
        channel = client.get_channel(config.botConfig["error-channel-id"])
        error_message = f"An error occurred:\n```{traceback.format_exc()}```"
        await channel.send(error_message)
    async def on_error(self, event, *args, **kwargs):
        await self.send_error_message(traceback.format_exc())

client = Client()
client.run(config.botConfig["token"])
