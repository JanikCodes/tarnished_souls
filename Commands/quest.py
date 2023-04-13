import discord
from discord import app_commands
from discord.ext import commands

import db
from Classes.user import User
from Utils.classes import class_selection


class Quest(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="quest", description="Try completing the quest-line")
    async def quest(self, interaction: discord.Interaction):
        if db.validate_user(interaction.user.id):
            user = User(interaction.user.id)
            
            embed = discord.Embed(title=f"Current Quest",
                                  description=f"**<@{user.get_userId()}>** ")

            embed.set_footer(text="You can earn more while defeating enemies or doing /explore")

            await interaction.response.send_message(embed=embed)
        else:
            await class_selection(interaction=interaction)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Quest(client), guild=discord.Object(id=763425801391308901))
