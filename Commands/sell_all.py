import discord
from discord import app_commands
from discord.ext import commands

import db
from Classes.item import Item
from Classes.user import User
from Utils.classes import class_selection


class SellAllButton(discord.ui.Button):

    def __init__(self, user, label, items, amount, value, duplicates):
        super().__init__(label=f"Sell {amount} {label} for {value} runes", style=discord.ButtonStyle.danger)
        self.user = user
        self.items = items
        self.amount = amount
        self.title = label
        self.value = value
        self.duplicates = duplicates

    async def callback(self, interaction: discord.Interaction):
        try:
            if interaction.user.id != int(self.user.get_userId()):
                embed = discord.Embed(title=f"You're not allowed to use this action!",
                                      description="",
                                      colour=discord.Color.red())
                return await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=2)

            await interaction.response.defer()

            message = interaction.message
            edited_embed = message.embeds[0]
            edited_embed.colour = discord.Color.green()

            for item in self.items:
                sell_item = db.get_item_from_user_with_id_rel(idUser=self.user.get_userId(), idRel=item.get_idRel())
                if sell_item and not self.duplicates:
                    if sell_item.get_count() >= item.get_count():
                        db.decrease_item_from_user(idUser=self.user.get_userId(), relId=sell_item.get_idRel(),
                                                   amount=item.get_count())
                        db.increase_runes_from_user_with_id(self.user.get_userId(),
                                                            sell_item.get_price() * item.get_count())
                        db.check_for_quest_update(idUser=self.user.get_userId(),
                                                  runes=sell_item.get_price() * item.get_count())
                    else:
                        edited_embed.colour = discord.Color.red()
                        edited_embed.set_footer(
                            text=f"You no longer have any {self.title.lower()} duplicates to sell..")
                        await interaction.message.edit(embed=edited_embed, view=None)
                        return
                elif sell_item and sell_item.get_count() != 1:
                    db.decrease_item_from_user(idUser=self.user.get_userId(), relId=sell_item.get_idRel(),
                                               amount=item.get_count())
                    db.increase_runes_from_user_with_id(self.user.get_userId(),
                                                        sell_item.get_price() * item.get_count())
                    db.check_for_quest_update(idUser=self.user.get_userId(),
                                              runes=sell_item.get_price() * item.get_count())
                else:
                    match self.duplicates:
                        case True:
                            edited_embed.colour = discord.Color.red()
                            edited_embed.set_footer(
                                text=f"You no longer have any {self.title.lower()} duplicates to sell..")
                            await interaction.message.edit(embed=edited_embed, view=None)
                            return
                        case False:
                            edited_embed.colour = discord.Color.red()
                            if self.title == "Items":
                                edited_embed.set_footer(
                                    text=f"You no longer have any {self.title[:-1].lower()} to sell..")
                            else:
                                edited_embed.set_footer(text=f"You no longer have any {self.title.lower()} to sell..")
                            await interaction.message.edit(embed=edited_embed, view=None)
                            return

            match self.duplicates:
                case True:
                    match self.title:
                        case "Weapons":
                            edited_embed.title = f"**All {self.title.lower()} duplicates have been sold!**"
                        case "Armor":
                            edited_embed.title = f"**All {self.title.lower()} duplicates has been sold!**"
                        case "Items":
                            edited_embed.title = f"**All {self.title[:-1].lower()} duplicates have been sold!**"
                case False:
                    match self.title:
                        case "Weapons":
                            edited_embed.title = f"**All {self.title.lower()} have been sold!**"
                        case "Armor":
                            edited_embed.title = f"**All {self.title.lower()} has been sold!**"
                        case "Items":
                            edited_embed.title = f"**All {self.title.lower()} have been sold!**"
            edited_embed.set_field_at(index=0, name="Amount of items:",
                                      value=f"{self.amount}\n\nYou received {self.value} runes!")

            await interaction.message.edit(embed=edited_embed, view=None)
        except discord.errors.NotFound:
            pass


class SellAllView(discord.ui.View):

    def __init__(self, user, label, items, amount, value, duplicates):
        super().__init__()
        self.user = user.update_user()
        self.add_item(
            SellAllButton(user=self.user, label=label, items=items, amount=amount, value=value, duplicates=duplicates))


class SellAll(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="sell_all", description="Sell all except equipped of your items")
    @app_commands.choices(choices=[
        app_commands.Choice(name="Weapons", value="Weapon"),
        app_commands.Choice(name="Armor", value="Armor"),
        app_commands.Choice(name="Items", value="Item")
    ])
    @app_commands.describe(duplicates="Select True if you want to sell duplicates ONLY. False if ALL.")
    async def sell_all(self, interaction: discord.Interaction, choices: app_commands.Choice[str], duplicates: bool = None):
        if not interaction or interaction.is_expired():
            return

        try:
            await interaction.response.defer()

            self.client.add_to_activity()

            if db.validate_user(interaction.user.id):
                user = User(userId=interaction.user.id)
                items = db.get_all_items_from_user(user.get_userId(), choices.value)

                if items:
                    embed = discord.Embed(title=f"Do you want to sell all {choices.name.lower()}?")
                    match choices.value:
                        case "Weapon":
                            embed.set_thumbnail(url=Item(idItem=5).get_icon_url())
                        case "Armor":
                            embed.set_thumbnail(url=Item(idItem=308).get_icon_url())
                        case "Item":
                            embed.set_thumbnail(url=Item(idItem=851).get_icon_url())
                    embed.color = discord.Color.orange()
                    if choices.value != "Item":
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
                            embed.add_field(name="Amount of items:", value=amount)
                            embed.description = f"This action __will sell **ALL**__ your {choices.name.lower()}.\n***Only __duplicates__***"
                            embed.set_footer(text="Except your currently equipped ones.")
                            await interaction.followup.send(embed=embed,
                                                            view=SellAllView(user=user, label=choices.name,
                                                                             items=items, amount=amount,
                                                                             value=value, duplicates=True))
                        else:
                            new_embed = discord.Embed(title=f"You don't have any {choices.name.lower()} duplicates..",
                                                      description="", colour=discord.Color.red())
                            if choices.value != "Armor":
                                new_embed.title = f"You don't have any {choices.name[:-1].lower()} duplicates.."
                            await interaction.followup.send(
                                embed=new_embed)
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
                                                                         value=value, duplicates=False))
                else:
                    embed = discord.Embed(title=f"You don't have any {choices.name.lower()} to sell..")
                    embed.color = discord.Color.red()
                    embed.description = ""
                    await interaction.followup.send(embed=embed)
            else:
                await class_selection(interaction=interaction)
                return
        except Exception as e:
            await self.client.send_error_message(e)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(SellAll(client))
