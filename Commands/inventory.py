import discord
from discord import app_commands
from discord.ext import commands

import db
from Classes.user import User

MAX_ITEM_FOR_PAGE = 3

class InventoryPageButton(discord.ui.Button):
    def __init__(self, text, direction, user, func, last_page, total_page_count):
        super().__init__(label=text, style=discord.ButtonStyle.secondary, disabled=False)
        self.direction = direction
        self.user = user
        self.func = func
        self.last_page = last_page
        self.total_page_count = total_page_count

        if direction == 'prev':
            if last_page == 1:
                self.disabled = True
        elif direction == 'next':
            if total_page_count == last_page:
                self.disabled = True

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != int(self.user.get_userId()):
            embed = discord.Embed(title=f"You're not allowed to use this action!",
                                  description="",
                                  colour=discord.Color.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        await interaction.response.defer()

        if self.direction == 'next':
            await view_inventory_page(interaction=interaction, user=self.user, page=self.last_page+1, label=self.func)
        elif self.direction == 'prev':
            await view_inventory_page(interaction=interaction, user=self.user, page=self.last_page-1, label=self.func)
            pass

class InventoryReturnButton(discord.ui.Button):
    def __init__(self, text, user):
        super().__init__(label=text, style=discord.ButtonStyle.danger)
        self.user = user

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != int(self.user.get_userId()):
            embed = discord.Embed(title=f"You're not allowed to use this action!",
                                  description="",
                                  colour=discord.Color.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        await interaction.response.defer()

        default_embed = discord.Embed(title=f" {self.user.get_userName()}'s Inventory",
                              description="Please select an inventory category below!")
        default_embed.colour = discord.Color.green()
        default_embed.set_footer(text="You'll unlock more items & titles while playing!")

        await interaction.message.edit(embed=default_embed, view=DefaultInventoryView(user=self.user))


class ItemInventoryView(discord.ui.View):
    def __init__(self, user, func, current_page, total_page_count):
        super().__init__()
        self.user = user.update_user()
        self.add_item(InventoryReturnButton(text="Return", user=user))
        self.add_item(InventoryPageButton(text="Previous",direction="prev", user=user, func=func, last_page=current_page, total_page_count=total_page_count))
        self.add_item(InventoryPageButton(text="Next", direction="next", user=user, func=func, last_page=current_page, total_page_count=total_page_count))

class InventoryCategoryButton(discord.ui.Button):
    def __init__(self, text, button_style, func, user):
        super().__init__(label=text, style=button_style)
        self.func = func
        self.user = user


    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != int(self.user.get_userId()):
            embed = discord.Embed(title=f"You're not allowed to use this action!",
                                  description="",
                                  colour=discord.Color.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        await interaction.response.defer()

        await view_inventory_page(interaction=interaction, label=self.func,user=self.user, page=1)


async def view_inventory_page(interaction, label, user, page):
    new_embed = discord.Embed(title=f"Inventory '{label}'", description="Below are your items sorted by their value (*damage/armor*).")
    new_embed.colour = discord.Color.light_embed()

    items = db.get_items_from_user_id_with_type_at_page(idUser=user.get_userId(), type=label, page=page, max_page=MAX_ITEM_FOR_PAGE)
    item_count = db.get_item_count_from_user(idUser=user.get_userId(), type=label)
    total_page_count = (int(item_count) + MAX_ITEM_FOR_PAGE - 1) // MAX_ITEM_FOR_PAGE

    if items:
        match label:
            case "weapon":
                for item in items:
                    emoji = discord.utils.get(interaction.client.get_guild(763425801391308901).emojis, name=item.get_iconCategory())

                    new_embed.add_field(name=f"{emoji} __{item.get_count()}x {item.get_name()}__ `id: {item.get_idRel()}`",
                                        value=f"**Statistics:** \n"
                                              f"`Damage:` **{item.get_total_value()}** `Weight:` **{item.get_weight()}**\n"
                                              f"**Requirements:** \n"
                                              f"{item.get_requirement_text(user)}",
                                        inline=False)
            case "armor":
                for item in items:
                    emoji = discord.utils.get(interaction.client.get_guild(763425801391308901).emojis, name=item.get_iconCategory())

                    new_embed.add_field(name=f"{emoji} __{item.get_count()}x {item.get_name()}__ `id: {item.get_idRel()}`",
                                        value=f"**Statistics:** \n"
                                              f"`Armor:` **{item.get_total_value()}** `Weight:` **{item.get_weight()}**\n",
                                        inline=False)
            case "title":
                pass


    new_embed.set_footer(text=f"Page {page}/{str(total_page_count)}")

    await interaction.message.edit(embed=new_embed, view=ItemInventoryView(user=user, func=label, current_page=page, total_page_count=total_page_count))

class DefaultInventoryView(discord.ui.View):

    def __init__(self, user):
        super().__init__()
        self.user = user.update_user()
        self.add_item(InventoryCategoryButton(text="Weapons", button_style=discord.ButtonStyle.danger, func="weapon", user=user))
        self.add_item(InventoryCategoryButton(text="Armor", button_style=discord.ButtonStyle.secondary, func="armor", user=user))
        self.add_item(InventoryCategoryButton(text="Titles", button_style=discord.ButtonStyle.success, func="title", user=user))

class Inventory(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="inventory", description="Display your inventory")
    async def inventory(self, interaction: discord.Interaction):
        db.validate_user(interaction.user.id, interaction.user.name)
        user = User(interaction.user.id)

        embed = discord.Embed(title=f" {user.get_userName()}'s Inventory", description="Please select an inventory category below!")
        embed.colour = discord.Color.green()
        embed.set_footer(text="You'll unlock more items & titles while playing!")
        await interaction.response.send_message(embed=embed, view=DefaultInventoryView(user=user))

async def setup(client:commands.Bot) -> None:
    await client.add_cog(Inventory(client), guild=discord.Object(id=763425801391308901))
