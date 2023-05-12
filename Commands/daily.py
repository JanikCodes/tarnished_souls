import discord
from discord import app_commands
from discord.ext import commands

import config
import db


class DailyCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="daily", description="Get some daily rewards, tarnished!")
    async def daily(self, interaction: discord.Interaction):
        daily_embed = discord.Embed(title="daily reward(s):")
        daily_embed.colour = discord.Color.orange()

        await interaction.response.send_message(embed=daily_embed)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(DailyCommand(client))