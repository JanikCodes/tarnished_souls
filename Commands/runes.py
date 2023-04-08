import discord
from discord import app_commands
from discord.ext import commands

import db
from Classes.user import User
from Utils.classes import class_selection


class Runes(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="runes", description="Display your runes amount")
    async def runes(self, interaction: discord.Interaction):
        if db.validate_user(interaction.user.id):
            user = User(interaction.user.id)

            embed = discord.Embed(title=f" {user.get_userName()} runes",
                                  description=f"**{user.get_runes()}** runes")

            await interaction.response.send_message(embed=embed)
        else:
            await class_selection(interaction=interaction)

async def setup(client:commands.Bot) -> None:
    await client.add_cog(Runes(client), guild=discord.Object(id=763425801391308901))
