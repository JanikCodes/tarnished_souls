import discord
from discord import app_commands
from discord.ext import commands
from py_discord_db_management import dbpyman
from py_discord_db_management.classes.database import Database

import config
import db
from Utils.classes import class_selection


class FrameworkCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="framework", description="Developer only..")
    async def framework(self, interaction: discord.Interaction):
        if not interaction or interaction.is_expired():
            return

        try:
            if db.validate_user(interaction.user.id):

                if interaction.user.id in config.botConfig["developer-ids"]:

                    await interaction.response.defer()

                    self.client.add_to_activity()

                    database = Database(host=config.botConfig["host"],
                                        user=config.botConfig["user"],
                                        password=config.botConfig["password"],
                                        port=config.botConfig["port"],
                                        database_name=config.botConfig["database"],
                                        charset='utf8mb4')

                    database.set_table_hidden('enemy_logic')
                    database.set_table_hidden('item')
                    database.set_table_hidden('move_type')
                    database.set_table_hidden('quest_has_user')
                    database.set_table_hidden('quest_type')
                    database.set_table_hidden('user')
                    database.set_table_hidden('user_encounter')
                    database.set_table_hidden('user_has_quest')
                    # default values for enemy
                    database.set_column_default_value('enemy', 'idLogic', 1)
                    database.set_column_default_value('enemy', 'health', 0)
                    database.set_column_default_value('enemy', 'runes', 0)
                    database.set_column_default_value('enemy', 'idLocation', 1)
                    # default values for enemy_moves
                    database.set_column_default_value('enemy_moves', 'phase', 0)
                    database.set_column_default_value('enemy_moves', 'idType', 1)
                    database.set_column_default_value('enemy_moves', 'damage', 0)
                    database.set_column_default_value('enemy_moves', 'healing', 0)
                    database.set_column_default_value('enemy_moves', 'duration', 0)
                    database.set_column_default_value('enemy_moves', 'maxTargets', 4)
                    database.set_column_hidden('enemy_moves', 'damage')
                    database.set_column_hidden('enemy_moves', 'duration')
                    # default values for quest
                    database.set_column_default_value('quest', 'reqKills', 0)
                    database.set_column_default_value('quest', 'reqitemCount', 0)
                    database.set_column_default_value('quest', 'reqRunes', 0)
                    database.set_column_default_value('quest', 'idItem', None)
                    database.set_column_default_value('quest', 'idEnemy', None)
                    database.set_column_default_value('quest', 'runeReward', 0)
                    database.set_column_default_value('quest', 'locationIdReward', None)
                    database.set_column_default_value('quest', 'reqExploreCount', 0)
                    database.set_column_default_value('quest', 'locationId', None)
                    database.set_column_default_value('quest', 'cooldown', 0)
                    database.set_column_default_value('quest', 'flaskReward', 0)
                    database.set_column_default_value('quest', 'reqInvasionKills', 0)
                    database.set_column_default_value('quest', 'reqHordeWave', 0)



                    embed, view = dbpyman.create_db_management(database)

                    await interaction.followup.send(embed=embed, view=view)
                else:
                    await interaction.followup.send("You're not a developer!", ephemeral=True)
            else:
                await class_selection(interaction=interaction)
        except Exception as e:
            await self.client.send_error_message(e)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(FrameworkCommand(client))