import logging
import os
import platform
import time
import traceback
from datetime import datetime

import config
import discord
from colorama import Back, Fore, Style
from discord.ext import commands, tasks
import db

import unittest
from Tests.test import TestCases

UPDATE_ITEMS = True
FILL_FIRST_TIME_DATA = False


class Client(commands.Bot):
    def __init__(self):
        # intents = discord.Intents.default()
        # intents.members = True


        super().__init__(command_prefix='!-&%')
        self.activity_list = {i: 0 for i in range(24)}

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
        db.init_database(config.botConfig)

        logging.warning("Now logging..")

        if UPDATE_ITEMS:
            db.fill_db_weapons()
            print("Added weapon data..")
            db.fill_db_armor()
            print("Added armor data..")

        if FILL_FIRST_TIME_DATA:
            db.fill_db_init()
            print("Added init data..")

        print("Finished updating/adding data")
        self.username_upd_task.start()

    @tasks.loop(hours=24)
    async def username_upd_task(self):
        await db.update_usernames(self)

    def add_to_activity(self):
        hour = datetime.now().hour
        self.activity_list[hour] += 1


def __run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCases)

    runner = unittest.TextTestRunner()

    result = runner.run(suite)

    print("Number of tests run:", result.testsRun)
    print("Number of failures:", len(result.failures))
    print("Number of errors:", len(result.errors))

    if result.wasSuccessful():
        print("All tests passed successfully.")
        return True
    else:
        print("Some tests failed.")
        return False

if __run_tests():
    client = Client()
    client.run(config.botConfig["token"])
