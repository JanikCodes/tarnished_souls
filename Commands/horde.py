import discord
from discord import app_commands
from discord.ext import commands

import db
from Classes.user import User
from Commands.fight import Fight, FightLobbyView
from Utils.classes import class_selection

MAX_USERS = 4

class HordeCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="horde", description="Fight as long as you can!")
    async def horde(self, interaction: discord.Interaction):
        await interaction.response.defer()

        try:
            if db.validate_user(interaction.user.id):

                user = User(interaction.user.id)

                embed = discord.Embed(title=f"Public Lobby",
                                      description="",
                                      colour=discord.Color.orange())

                embed.add_field(name=f"Horde Mode 💀", value="Defeat as many enemies as you can without dying!")
                embed.add_field(name=f"Players: **1/{MAX_USERS}**", value="", inline=False)
                embed.set_footer(text="Enemy health is increased based on player count")

                enemy_list = db.get_all_enemies()

                await interaction.followup.send(embed=embed, view=FightLobbyView(users=[user], visibility="public", enemy_list=enemy_list))
            else:
                await class_selection(interaction=interaction)
        except Exception as e:
            await self.client.send_error_message(e)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(HordeCommand(client))
