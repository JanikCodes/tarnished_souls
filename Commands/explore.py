import discord
from discord import app_commands
from discord.ext import commands
import db
from Classes.user import User
from Utils import utils

class Explore(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="explore", description="Explore the world, encounter events & receive items and souls!")
    async def explore(self, interaction: discord.Interaction):
        db.validate_user(interaction.user.id, interaction.user.name)
        user = User(interaction.user.id)

        embed = discord.Embed(title=f" {user.get_userName()} started exploring...")

        await interaction.response.send_message(embed=embed)

async def setup(client:commands.Bot) -> None:
    await client.add_cog(Explore(client), guild=discord.Object(id=763425801391308901))
