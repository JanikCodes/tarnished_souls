import discord
from discord import app_commands
from discord.ext import commands

import db
from Classes.user import User
from Utils.classes import class_selection


class Runes(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.rename(optional_user='user')
    @app_commands.command(name="runes", description="Display your runes amount")
    @app_commands.checks.has_permissions(manage_messages=True, embed_links=True, add_reactions=True,
                                         external_emojis=True, read_message_history=True, read_messages=True,
                                         send_messages=True, use_application_commands=True, use_external_emojis=True)
    async def runes(self, interaction: discord.Interaction, optional_user: discord.Member = None):
        if not interaction or interaction.is_expired():
            return

        try:
            await interaction.response.defer()

            self.client.add_to_activity()

            if db.validate_user(interaction.user.id):

                if optional_user:
                    # check if user exists in db
                    if db.validate_user(userId=optional_user.id):
                        user = User(optional_user.id)
                    else:
                        embed = discord.Embed(title=f"User doesn't exist yet..",
                                              description="The user needs to choose a class first by typing any command like `/explore` or `/quest`",
                                              colour=discord.Color.red())
                        return await interaction.followup.send(embed=embed)
                else:
                    user = User(interaction.user.id)

                embed = discord.Embed(title=f"{user.get_userName()} rune amount",
                                      description=f"**{user.get_runes()}** runes")

                embed.set_footer(text="You can earn more while defeating enemies or doing /explore")

                await interaction.followup.send(embed=embed)
            else:
                await class_selection(interaction=interaction)
        except Exception as e:
            await self.client.send_error_message(e)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Runes(client))
