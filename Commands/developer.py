import discord
from discord import app_commands
from discord.ext import commands

import db
from Classes.user import User
from Utils.classes import class_selection


class CompleteQuestButton(discord.ui.Button):
    def __init__(self, user):
        super().__init__(label="Complete Quest", style=discord.ButtonStyle.success)
        self.user = user

    async def callback(self, interaction: discord.Interaction):

        if interaction.user.id != int(self.user.get_userId()):
            embed = discord.Embed(title=f"You're not allowed to use this action!",
                                  description="",
                                  colour=discord.Color.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=2)

        await interaction.response.defer()

        db.complete_quest(user=self.user)

class DeveloperView(discord.ui.View):

    def __init__(self, user):
        super().__init__()
        self.user = user.update_user()
        self.add_item(CompleteQuestButton(user=user))

class Developer(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="developer", description="Developer only.. sorry")
    async def developer(self, interaction: discord.Interaction):
        try:
            if db.validate_user(interaction.user.id):

                await interaction.response.defer()

                user = User(interaction.user.id)

                if interaction.user.id == 321649314382348288:

                    embed = discord.Embed(title=f"Developer options",
                                          description="")
                    embed.add_field(name="Servers", value=f"{len(self.client.guilds)}")
                    embed.add_field(name="Users", value=f"{db.get_all_user_count()}")
                    embed.add_field(name="AVG Quest", value=f"{db.get_avg_user_quest()}")

                    await interaction.followup.send(embed=embed, view=DeveloperView(user=user))
                else:
                    await interaction.followup.send("You're not a developer!", ephemeral=True)
            else:
                await class_selection(interaction=interaction)
        except Exception as e:
            await self.client.send_error_message(e)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Developer(client))
