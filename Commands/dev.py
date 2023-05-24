import discord
from discord import app_commands
from discord.ext import commands
from py_discord_db_management import dbpyman
from py_discord_db_management.classes.database import Database

import config


class DevCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="dev", description="Lmao.")
    async def dev(self, interaction: discord.Interaction):
        if not interaction or interaction.is_expired():
            return

        try:
            await interaction.response.defer()

            self.client.add_to_activity()

            database = Database(host=config.botConfig["host"],
                                user=config.botConfig["user"],
                                password=config.botConfig["password"],
                                port=config.botConfig["port"],
                                database_name=config.botConfig["database"],
                                charset='utf8mb4')

            embed, view = dbpyman.create_db_management(database)

            await interaction.followup.send(embed=embed, view=view)
        except Exception as e:
            await self.client.send_error_message(e)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(DevCommand(client))
