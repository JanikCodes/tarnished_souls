import discord
from discord import app_commands
from discord.ext import commands

import db
from Classes.user import User
from Utils.classes import class_selection


class Favorite(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="favorite", description="Mark one of your items are favorite!")
    async def favorite(self, interaction: discord.Interaction, id: int ):
        print("Favorite")
        if not interaction or interaction.is_expired():
            return

        try:
            await interaction.response.defer()

            self.client.add_to_activity()

            if db.validate_user(interaction.user.id):

                user = User(interaction.user.id)

                item = db.get_item_from_user_with_id_rel(idUser=user.get_userId(), idRel=id)

                if item:
                    if item.get_favorite() != 1:
                        db.set_item_from_user_favorite(idUser=user.get_userId(), idRel=id, favorite=True)

                        embed = discord.Embed(title=f"{item.get_name()} has been marked as favorite!",
                                              description="It will be excluded from the `sell` commands.", colour=discord.Color.green())
                        embed.set_thumbnail(url=item.get_icon_url())

                        await interaction.followup.send(embed=embed)
                    else:
                        embed = discord.Embed(title=f"{item.get_name()} is already marked as favorite!", description="", colour=discord.Color.red())

                        await interaction.followup.send(embed=embed)

                else:
                    embed = discord.Embed(title=f"I couldn't find the correct Item..",
                                          description=f"You can find your Item Id inside your inventory. Access it with `/inventory`",
                                          colour=discord.Color.red())
                    await interaction.followup.send(embed=embed, ephemeral=True)
            else:
                await class_selection(interaction=interaction)
        except Exception as e:
            await self.client.send_error_message(e)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Favorite(client))