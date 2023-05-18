import discord
from discord import app_commands
from discord.ext import commands

import config
import db
from Classes.user import User
from Utils.classes import class_selection


class SellButton(discord.ui.Button):
    def __init__(self, user, item, amount, disabled=False):
        super().__init__(label=f"Sell {amount}x ({item.get_price() * amount} runes)", style=discord.ButtonStyle.danger,
                         disabled=disabled)
        self.user = user
        self.item = item
        self.amount = amount

    async def callback(self, interaction: discord.Interaction):
        try:
            if interaction.user.id != int(self.user.get_userId()):
                embed = discord.Embed(title=f"You're not allowed to use this action!",
                                      description="",
                                      colour=discord.Color.red())
                return await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=2)

            await interaction.response.defer()

            sell_item = db.get_item_from_user_with_id_rel(idUser=self.user.get_userId(), idRel=self.item.get_idRel())
            if sell_item:
                if sell_item.get_count() >= self.amount:
                    db.decrease_item_from_user(idUser=self.user.get_userId(), relId=sell_item.get_idRel(),
                                               amount=self.amount)
                    db.increase_runes_from_user_with_id(self.user.get_userId(), self.item.get_price() * self.amount)
                    db.check_for_quest_update(idUser=self.user.get_userId(), runes=self.item.get_price() * self.amount)
                    message = interaction.message
                    edited_embed = message.embeds[0]
                    edited_embed.colour = discord.Color.green()

                    if sell_item.get_count() - self.amount > 0:
                        edited_embed.title = f"**{sell_item.get_name()}** {sell_item.get_count() - self.amount}x `id: {sell_item.get_idRel()}`"
                        await interaction.message.edit(embed=edited_embed,
                                                       view=SellView(user=self.user, item=self.item))
                    else:
                        # completely sold
                        edited_embed.title = f"**{sell_item.get_name()}**"
                        edited_embed.description = "Completely sold this item!"
                        await interaction.message.edit(embed=edited_embed, view=None)
                else:
                    message = interaction.message
                    edited_embed = message.embeds[0]
                    edited_embed.colour = discord.Color.red()
                    edited_embed.set_footer(text="This item no longer exists with that item quantity..")

                    await interaction.message.edit(embed=edited_embed, view=None)
            else:
                message = interaction.message
                edited_embed = message.embeds[0]
                edited_embed.colour = discord.Color.red()
                edited_embed.set_footer(text="This item no longer exists..")

                await interaction.message.edit(embed=edited_embed, view=None)
        except discord.errors.NotFound:
            pass


class SellAllButton(discord.ui.Button):

    def __init__(self, user, label, items, amount, value):
        super().__init__(label=f"Sell {amount} {label} for {value} runes", style=discord.ButtonStyle.danger)
        self.user = user
        self.items = items
        self.amount = amount
        self.title = label
        self.value = value

    async def callback(self, interaction: discord.Interaction):
        try:
            if interaction.user.id != int(self.user.get_userId()):
                embed = discord.Embed(title=f"You're not allowed to use this action!",
                                      description="",
                                      colour=discord.Color.red())
                return await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=2)

            await interaction.response.defer()

            for item in self.items:
                sell_item = db.get_item_from_user_with_id_rel(idUser=self.user.get_userId(), idRel=item.get_idRel())
                if sell_item:
                    db.decrease_item_from_user(idUser=self.user.get_userId(), relId=sell_item.get_idRel(), amount=item.get_count())
                    db.increase_runes_from_user_with_id(self.user.get_userId(), sell_item.get_price() * item.get_count())
                    db.check_for_quest_update(idUser=self.user.get_userId(), runes=sell_item.get_price() * item.get_count())

            message = interaction.message
            edited_embed = message.embeds[0]
            edited_embed.colour = discord.Color.green()
            edited_embed.description = ""
            edited_embed.remove_field(0)
            edited_embed.set_footer(text=f"You received {self.value} runes!")
            edited_embed.set_thumbnail(url="")
            match self.title:
                case "Weapons":
                    edited_embed.title = f"**All {self.title} have been sold!**"
                case "Armor":
                    edited_embed.title = f"**All {self.title} has been sold!**"
                case "Items":
                    edited_embed.title = f"**All {self.title} have been sold!**"
            await interaction.message.edit(embed=edited_embed, view=None)
        except discord.errors.NotFound:
            pass


class SellView(discord.ui.View):

    def __init__(self, user, item):
        super().__init__()
        self.user = user.update_user()
        item = db.get_item_from_user_with_id_rel(user.get_userId(), item.get_idRel())
        self.add_item(SellButton(user=user, item=item, amount=1, disabled=False if item.get_count() >= 1 else True))
        self.add_item(SellButton(user=user, item=item, amount=5, disabled=False if item.get_count() >= 5 else True))


class SellAllView(discord.ui.View):

    def __init__(self, user, label, items, amount, value):
        super().__init__()
        self.user = user.update_user()
        self.add_item(SellAllButton(user=self.user, label=label, items=items, amount=amount, value=value))


class Sell(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="sell", description="Sell one of your items")
    @app_commands.describe(item_id="Enter an item id")
    @app_commands.rename(item_id='id')
    async def sell(self, interaction: discord.Interaction, item_id: int = None):
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
                    embed = discord.Embed(title=f"**{item.get_name()}** {item.get_count()}x `id: {item.get_idRel()}`",
                                          description=f"Do you want to sell this item?")

                    if item.get_icon_url() is not None and item.get_icon_url() != 'None':
                        embed.set_thumbnail(url=f"{item.get_icon_url()}")

                    match item.get_item_type():
                        case 'Weapon':
                            embed.add_field(name="", value=f"**Statistics:** \n"
                                                           f"`Damage:` **{item.get_total_value(user)}** `Weight:` **{item.get_weight()}**",
                                            inline=False)
                        case 'Armor':
                            embed.add_field(name="", value=f"**Statistics:** \n"
                                                           f"`Armor:` **{item.get_total_value(user)}** `Weight:` **{item.get_weight()}**",
                                            inline=False)
                        case 'Item':
                            embed.add_field(name="", value=f"**Information:** \n"
                                                           f"It's a material that is used for smithing weapons..",
                                            inline=False)

                    embed.colour = discord.Color.orange()

                    await interaction.followup.send(embed=embed, view=SellView(user=user, item=item))
            else:
                await class_selection(interaction=interaction)
        except Exception as e:
            await self.client.send_error_message(e)

    @app_commands.command(name="sell_all", description="Sell all except equipped of your items")
    @app_commands.choices(choices=[
        app_commands.Choice(name="Weapons", value="Weapon"),
        app_commands.Choice(name="Armor", value="Armor"),
        app_commands.Choice(name="Item", value="Item")
    ])
    @app_commands.describe(duplicates="Select True if you want to sell duplicates ONLY. False if ALL.")
    async def sell_all(self, interaction: discord.Interaction, choices: app_commands.Choice[str], duplicates: bool=None):
        try:
            await interaction.response.defer()

            self.client.add_to_activity()

            if db.validate_user(interaction.user.id):
                user = User(userId=interaction.user.id)
                items = db.get_all_items_from_user(user.get_userId(), choices.value)
                if items:
                    embed = discord.Embed(title=f"Sell all {choices.name}")
                    match choices.value:
                        case "Weapon":
                            embed.set_thumbnail(url=db.get_item_from_item_id(5).get_icon_url())
                        case "Armor":
                            embed.set_thumbnail(url=db.get_item_from_item_id(308).get_icon_url())
                        case "Item":
                            embed.set_thumbnail(url=db.get_item_from_item_id(851).get_icon_url())
                    embed.color = discord.Color.orange()
                    if choices.value == "Item":
                        embed.description = "Sell all your items."
                    else:
                        embed.description = f"This action __will sell **ALL**__ your {choices.name}."
                    embed.set_footer(text="Except your currently equipped ones.")

                    value = int()
                    amount = int()

                    if duplicates:
                        i = 0
                        while i < len(items):
                            item = items[i]
                            if item.get_count() > 1:
                                count = abs(item.get_count() - 1)
                                value += item.get_price() * count
                                item.set_count(count)
                                amount += item.get_count()
                                i += 1
                            else:
                                items.remove(item)

                        if len(items) != 0:
                            embed.color = discord.Color.yellow()
                            embed.add_field(name="Amount of items:", value=amount)
                            embed.description = f"This action __will sell **ALL**__ your {choices.name}.\n***Only __duplicates__***"
                            embed.set_footer(text="Except your currently equipped ones.")
                            await interaction.followup.send(embed=embed,
                                                                    view=SellAllView(user=user, label=choices.name,
                                                                                     items=items, amount=amount,
                                                                                     value=value))
                        else:
                            await interaction.followup.send(
                                embed=discord.Embed(title="You don't have any duplicates..", description="",
                                                    colour=discord.Color.red()))
                    else:
                        for item in items:
                            if item.get_count() > 1:
                                value += item.get_price() * item.get_count()
                            else:
                                value += item.get_price()
                            amount += item.get_count()

                        embed.add_field(name="Amount of items:", value=amount)
                        await interaction.followup.send(embed=embed,
                                                                view=SellAllView(user=user, label=choices.name,
                                                                                 items=items, amount=amount,
                                                                                 value=value))
                else:
                    embed = discord.Embed(title=f"You don't have any {choices.name} to sell..")
                    embed.color = discord.Color.red()
                    embed.description = ""
                    await interaction.followup.send(embed=embed)
            else:
                await class_selection(interaction=interaction)
                return
        except Exception as e:
            await self.client.send_error_message(e)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Sell(client), guild=discord.Object(id=config.botConfig["hub-server-guild-id"]))
