import discord
from discord import app_commands
from discord.ext import commands
import db
from Classes.user import User


class UpgradeStatsView(discord.ui.View):
    @discord.ui.button(label="Upgrade", row=0, style=discord.ButtonStyle.primary)
    async def upgrade_button_callback(self, button, interaction):
        await interaction.response.send_message("You upgraded your stat!")

class UpgradeStats(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="upgrade", description="Upgrade one of your available stats")
    @app_commands.choices(choices=[
        app_commands.Choice(name="Vigor", value="vigor"),
        app_commands.Choice(name="Mind", value="mind"),
        app_commands.Choice(name="Endurance", value="endurance"),
        app_commands.Choice(name="Strength", value="strength"),
        app_commands.Choice(name="Dexterity", value="dexterity"),
        app_commands.Choice(name="Intelligence", value="intelligence"),
        app_commands.Choice(name="Faith", value="faith"),
        app_commands.Choice(name="Arcane", value="arcane"),
    ])
    async def upgradeStats(self,  interaction: discord.Interaction, choices: app_commands.Choice[str]):
        db.validate_user(interaction.user.id, interaction.user.name)
        user = User(interaction.user.id)
        selectedChoice = choices.value

        embed = discord.Embed(title=f"Upgrade {selectedChoice}", description=f"Do you want to upgrade {selectedChoice}?")
        embed.set_author(name=user.get_userName())

        await interaction.response.send_message(embed=embed, view=UpgradeStatsView())

async def setup(client:commands.Bot) -> None:
    await client.add_cog(UpgradeStats(client), guild=discord.Object(id=763425801391308901))
