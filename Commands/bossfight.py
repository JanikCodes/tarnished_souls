import discord
from discord import app_commands
from discord.ext import commands

import db
from Classes.user import User


class Bossfight(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="startboss", description="Start a boss fight!")
    @app_commands.choices(choices=[
        app_commands.Choice(name="Public", value="public"),
        app_commands.Choice(name="Private", value="private"),
    ])
    async def startboss(self, interaction: discord.Interaction, choices: app_commands.Choice[str]):
        db.validate_user(interaction.user.id, interaction.user.name)
        user = User(interaction.user.id)
        selected_choice = choices.value

        embed = discord.Embed(title=f" {user.get_userName()} is starting a {selected_choice} boss fight!",
                              description="",
                              colour=discord.Color.orange())
        embed.set_footer(text="Click the button below in order to join!")

        await interaction.response.send_message(embed=embed)

async def setup(client:commands.Bot) -> None:
    await client.add_cog(Bossfight(client), guild=discord.Object(id=763425801391308901))
