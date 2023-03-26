import discord
from discord import app_commands
from discord.ext import commands
import db
from Classes.user import User

class UpgradeStats(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="upgrade", description="Upgrade one of your available stats")
    async def UpgradeStats(self,  interaction: discord.Interaction):
        db.validate_user(interaction.user.id, interaction.user.name)
        user = User(interaction.user.id)

        embed = discord.Embed(title="Upgrade X", description='Do you want to upgrade x?')
        embed.set_author(name=user.get_userName())

        await interaction.response.send_message(embed=embed)

async def setup(client:commands.Bot) -> None:
    await client.add_cog(UpgradeStats(client))
