import discord
from discord import app_commands
from discord.ext import commands

import db
from Classes.user import User
from Utils.classes import class_selection


class EquipButton(discord.ui.Button):
    def __init__(self, user, item, disabled=False):
        super().__init__(label='Equip', style=discord.ButtonStyle.success, disabled=disabled)
        self.user = user
        self.item = item

    async def callback(self, interaction: discord.Interaction):

        if interaction.user.id != int(self.user.get_userId()):
            embed = discord.Embed(title=f"You're not allowed to use this action!",
                                  description="",
                                  colour=discord.Color.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=2)

        await interaction.response.defer()

        suc = db.equip_item(idUser=self.user.get_userId(), item=self.item)
        if suc:
            message = interaction.message
            edited_embed = message.embeds[0]
            edited_embed.colour = discord.Color.green()
            edited_embed.set_footer(text="Successfully equipped!")

            await interaction.message.edit(embed=edited_embed, view=None, delete_after=2)
        else:
            message = interaction.message
            edited_embed = message.embeds[0]
            edited_embed.colour = discord.Color.red()

            await interaction.message.edit(embed=edited_embed, view=EquipView(user=self.user, item=self.item))


class EquipView(discord.ui.View):

    def __init__(self, user, item):
        super().__init__()
        self.user = user.update_user()
        self.add_item(EquipButton(user=user, item=item, disabled=not user.get_is_required_for_item(item)))


class Equip(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="equip", description="Equip one of your items with an item id.")
    @app_commands.describe(
        item_id="Enter an item id",
    )
    @app_commands.rename(item_id='id')
    async def equip(self, interaction: discord.Interaction, item_id: int):
        if not interaction or interaction.is_expired():
            return

        try:
            await interaction.response.defer()

            self.client.add_to_activity()

            if db.validate_user(interaction.user.id):

                user = User(interaction.user.id)
                item = db.get_item_from_user_with_id_rel(user.get_userId(), item_id)
                if item is None:
                    embed = discord.Embed(title=f"I couldn't find the correct Item..",
                                          description=f"You can find your Item Id inside your inventory. Access it with `/inventory`",
                                          colour=discord.Color.red())
                    await interaction.followup.send(embed=embed, ephemeral=True)
                else:
                    if item.get_item_type() == "Item":
                        embed = discord.Embed(title=f"This.. doesn't seem like something you would equip..",
                                              description=f"Nice try tho.",
                                              colour=discord.Color.red())
                        return await interaction.followup.send(embed=embed, ephemeral=True)

                    embed = discord.Embed(title=f"**{item.get_name()}** `id: {item.get_idRel()}`",
                                          description=f"Do you want to equip this item?")

                    if item.get_icon_url() is not None and item.get_icon_url() != 'None':
                        embed.set_thumbnail(url=f"{item.get_icon_url()}")

                    value_name = str()

                    match item.get_item_type():
                        case 'Weapon':
                            value_name = "Damage"
                        case 'Armor':
                            value_name = "Armor"

                    embed.add_field(name="", value=f"**Statistics:** \n"
                                                   f"`{value_name}:` **{item.get_total_value(user)}** `Weight:` **{item.get_weight()}**", inline=False)
                    embed.add_field(name="", value=f"**Requirements** \n"
                                                   f"{item.get_requirement_text()}", inline=False)

                    embed.colour = discord.Color.orange()

                    # user doesnt met requirements
                    if not user.get_is_required_for_item(item):
                        embed.colour = discord.Color.red()
                        embed.set_footer(text=f"You don't meet the requirements!")

                    await interaction.followup.send(embed=embed, view=EquipView(user=user, item=item))
            else:
                await class_selection(interaction=interaction)
        except Exception as e:
            await self.client.send_error_message(e)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Equip(client))
