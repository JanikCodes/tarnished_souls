import discord
from discord import app_commands
from discord.ext import commands
import db
from Classes.user import User


class InventoryPageButton(discord.ui.Button):
    def __init__(self, text, direction, user, disabled):
        super().__init__(label=text, style=discord.ButtonStyle.secondary, disabled=disabled)
        self.direction = direction
        self.user = user
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != int(self.user.get_userId()):
            return await interaction.response.send_message("You are not authorized to use this button.", ephemeral=True)

        await interaction.response.defer()


class WeaponInventoryView(discord.ui.View):
    def __init__(self, user):
        super().__init__()
        self.user = user.update_user()
        self.add_item(InventoryPageButton(text="Previous",direction="prev", user=user, disabled=True))
        self.add_item(InventoryPageButton(text="Next", direction="next", user=user, disabled=True))

class InventoryCategoryButton(discord.ui.Button):
    def __init__(self, text, button_style, func, user):
        super().__init__(label=text, style=button_style)
        self.func = func
        self.user = user


    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != int(self.user.get_userId()):
            return await interaction.response.send_message("You are not authorized to use this button.", ephemeral=True)

        await interaction.response.defer()


        if self.func == 'weapons':
            new_embed = discord.Embed(title="Inventory 'Weapons'", description="Below are your items sorted by their value (*damage/armor*).")
            new_embed.colour = discord.Color.light_embed()

            new_embed.set_footer(text="Page 1/1")
            await interaction.message.edit(embed=new_embed, view=WeaponInventoryView(user=self.user))
        elif self.func == 'armor':
            pass
        elif self.func == 'titles':
            pass

class DefaultInventoryView(discord.ui.View):

    def __init__(self, user):
        super().__init__()
        self.user = user.update_user()
        self.add_item(InventoryCategoryButton(text="Weapons", button_style=discord.ButtonStyle.danger, func="weapons", user=user))
        self.add_item(InventoryCategoryButton(text="Armor", button_style=discord.ButtonStyle.secondary, func="armor", user=user))
        self.add_item(InventoryCategoryButton(text="Titles", button_style=discord.ButtonStyle.success, func="titles", user=user))

class Inventory(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="inventory", description="Display your inventory")
    async def inventory(self, interaction: discord.Interaction):
        db.validate_user(interaction.user.id, interaction.user.name)
        user = User(interaction.user.id)

        embed = discord.Embed(title=f" {user.get_userName()} Inventory", description="Please select an inventory category below!")
        embed.colour = discord.Color.green()
        embed.set_footer(text="You'll unlock more items & titles while playing!")
        await interaction.response.send_message(embed=embed, view=DefaultInventoryView(user=user))

async def setup(client:commands.Bot) -> None:
    await client.add_cog(Inventory(client), guild=discord.Object(id=763425801391308901))
