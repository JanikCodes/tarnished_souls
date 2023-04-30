import discord
from discord import app_commands
from discord.ext import commands

import config
import db
from Classes.user import User
from Utils.classes import class_selection


class CompleteQuestButton(discord.ui.Button):
    def __init__(self, user):
        super().__init__(label="Complete Quest", style=discord.ButtonStyle.success)
        self.user = user

    async def callback(self, interaction: discord.Interaction):

        if not interaction.user.id in config.botConfig["developer-ids"]:
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
        await interaction.response.defer()

        try:
            if db.validate_user(interaction.user.id):

                user = User(interaction.user.id)

                if interaction.user.id in config.botConfig["developer-ids"]:

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
