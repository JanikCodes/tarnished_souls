import discord
from discord import app_commands
from discord.ext import commands

import db
from Classes.user import User
from Utils.classes import class_selection


class UnEquipButton(discord.ui.Button):
    def __init__(self, user, item):
        super().__init__(label='Equip', style=discord.ButtonStyle.success)
        self.user = user
        self.item = item

    async def callback(self, interaction: discord.Interaction):

        if interaction.user.id != int(self.user.get_userId()):
            embed = discord.Embed(title=f"You're not allowed to use this action!",
                                  description="",
                                  colour=discord.Color.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        await interaction.response.defer()


class UnEquipView(discord.ui.View):

    def __init__(self, user, item):
        super().__init__()
        self.user = user.update_user()
        self.add_item(UnEquipButton(user=user, item=item))


class UnEquip(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="unequip", description="Unequip one of your equipped items")
    @app_commands.choices(choices=[
        app_commands.Choice(name="Weapon", value="weapon"),
        app_commands.Choice(name="Helmet", value="head"),
        app_commands.Choice(name="Chest armor", value="chest"),
        app_commands.Choice(name="Gauntlets", value="gauntlet"),
        app_commands.Choice(name="Legs", value="legs"),
    ])
    async def unequip(self, interaction: discord.Interaction, choices: app_commands.Choice[str]):
        if db.validate_user(interaction.user.id):
            user = User(interaction.user.id)
            selected_choice = choices.value

            # TODO:
            # check if item is equipped at that slot
            # show that item and ask if he wants to unequip it
            # do it.

        else:
            await class_selection(interaction=interaction)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(UnEquip(client), guild=discord.Object(id=763425801391308901))
