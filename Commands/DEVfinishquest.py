import discord
from discord import app_commands
from discord.ext import commands

import db
from Classes.user import User
from Utils.classes import class_selection


class FinishQuest(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="finishquest", description="Developer only")
    async def finishquest(self, interaction: discord.Interaction):
        try:
            if db.validate_user(interaction.user.id):
                user = User(interaction.user.id)

                if user.get_userId() == 321649314382348288:
                    db.complete_quest(user=user)
                    await interaction.response.send_message("Completed quest!", ephemeral=True)
            else:
                await class_selection(interaction=interaction)
        except Exception as e:
            await self.client.send_error_message(e)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(FinishQuest(client))
