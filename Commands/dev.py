import config
import discord
from discord import app_commands
from discord.ext import commands
from py_discord_db_management import dbpyman
from py_discord_db_management.classes.database import Database


class DevCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="dev", description="WIP")
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

            database.set_table_hidden('user_has_item')
            database.set_table_hidden('user_has_quest')
            database.set_table_hidden('quest_has_item')
            database.set_table_hidden('quest_has_user')
            database.set_table_hidden('move_type')
            database.set_table_hidden('enemy_logic')
            database.set_table_hidden('quest_type')
            database.set_table_hidden('user')
            database.set_column_default_value('enemy_moves', 'phase', 0)
            database.set_column_default_value('enemy_moves', 'idType', 1)
            database.set_column_default_value('enemy_moves', 'damage', 0)
            database.set_column_default_value('enemy_moves', 'healing', 0)
            database.set_column_default_value('enemy_moves', 'duration', 0)
            database.set_column_default_value('enemy_moves', 'maxTargets', 4)
            database.set_column_hidden('enemy_moves', 'maxTargets')
            database.set_column_hidden('enemy_moves', 'damage')
            database.set_column_hidden('enemy_moves', 'healing')
            database.set_column_hidden('enemy_moves', 'phase')

            embed, view = dbpyman.create_db_management(database)

            await interaction.followup.send(embed=embed, view=view)
        except Exception as e:
            await self.client.send_error_message(e)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(DevCommand(client))
