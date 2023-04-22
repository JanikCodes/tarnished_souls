import discord
from discord import app_commands
from discord.ext import commands

import db
from Classes.user import User
from Utils.classes import class_selection


class Sell(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="sell", description="Sell a specific item!")
    async def sell(self, interaction: discord.Interaction):
        try:
            if db.validate_user(interaction.user.id):
                user = User(interaction.user.id)

                embed = discord.Embed(title=f"",
                                      description=f"")

                await interaction.response.send_message(embed=embed)
            else:
                await class_selection(interaction=interaction)
        except Exception as e:
            await self.client.send_error_message(e)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Sell(client))
