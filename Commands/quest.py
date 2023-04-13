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

            current_quest = db.get_user_quest_with_user_id(idUser=user.get_userId())

            if current_quest is None:
                # create new quest rel
                current_quest = db.add_init_quest_to_user(idUser=user.get_userId())

            embed = discord.Embed(title=f"{user.get_userName()}'s current quest:",
                                  description=f"**{current_quest.quest.get_title()}** \n{current_quest.quest.get_description()}")

            embed.add_field(name="Progress:", value=current_quest.get_quest_progress_text())

            await interaction.response.send_message(embed=embed)
        else:
            await class_selection(interaction=interaction)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Quest(client), guild=discord.Object(id=763425801391308901))
