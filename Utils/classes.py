import discord
import json
from discord import app_commands
from discord.ext import commands
import db
from Classes.user import User

class InventoryPageButton(discord.ui.Button):
    def __init__(self, text, direction, user, last_page, data):
        super().__init__(label=text, style=discord.ButtonStyle.secondary, disabled=False)
        self.direction = direction
        self.user = user
        self.last_page = last_page
        self.data = data

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user.id:
            embed = discord.Embed(title=f"You're not allowed to use this action!",
                                  description="",
                                  colour=discord.Color.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        await interaction.response.defer()

        if self.direction == 'next':
            new_index = 0 if self.last_page + 1 > (len(self.data) - 1) else self.last_page + 1
            await view_class_selection_page(interaction=interaction, data=self.data, index=new_index)
        elif self.direction == 'prev':
            new_index = (len(self.data) - 1) if self.last_page - 1 < 0 else self.last_page - 1
            await view_class_selection_page(interaction=interaction, data=self.data, index=new_index)


class ClassSelectionView(discord.ui.View):
    def __init__(self, user, current_page, data):
        super().__init__()
        self.user = user
        self.add_item(InventoryPageButton(text="Previous",direction="prev", user=user, last_page=current_page, data=data))
        self.add_item(InventoryPageButton(text="Next", direction="next", user=user, last_page=current_page, data=data))


async def class_selection(interaction: discord.Interaction):
    # read the JSON file
    with open('Data/classes.json', 'r') as f:
        data = json.load(f)

    await view_class_selection_page(interaction=interaction, data=data, index=0)


async def view_class_selection_page(interaction, data, index):

    embed = discord.Embed(title=f"Welcome! *please choose your start class!*",
                          description=f"")
    # iterate over the objects
    print(index)
    ed_class = data[index]

    class_name = ed_class['name'].replace("'", "''")
    class_desc = ed_class['description'].replace("'", "''")
    class_img_url = ed_class['image']

    embed.add_field(name=f"**{class_name}**", value=class_desc, inline=False)

    stat_text = str()
    eq_text = str()
    # add all the class stats
    for stat_name, stat_value in ed_class['stats'].items():
        stat_text += f"**{stat_name[:3].capitalize()}**: `{stat_value}` "

    for eq_name, eq_value in ed_class['equip'].items():
        if eq_name == "weapon":
            eq_text += f"**Weapon**: `{eq_value}` \n **Armor**: "
        else:
            if eq_value:
                eq_text += f" `{eq_value}` "

    embed.add_field(name="Statistics:", value=stat_text, inline=False)
    embed.add_field(name="Equipment:", value=eq_text, inline=False)

    embed.set_thumbnail(url=class_img_url)

    if interaction.message:
        await interaction.message.edit(embed=embed, view=ClassSelectionView(user=interaction.user, current_page=index, data=data))
    else:
        await interaction.response.send_message(embed=embed, view=ClassSelectionView(user=interaction.user, current_page=index, data=data))