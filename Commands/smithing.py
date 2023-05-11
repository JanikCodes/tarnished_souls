import discord
from discord import app_commands
from discord.ext import commands

import db
from Classes.user import User
from Utils.classes import class_selection


MATERIAL_TABLE = {
    1: 1001, 2: 1001, 3: 1001, 4: 1002, 5: 1002, 6: 1002, 7: 1003, 8: 1003, 9: 1003, 10: 1004,
    11: 1004, 12: 1004, 13: 1005, 14: 1005, 15: 1005, 16: 1006, 17: 1006, 18: 1006, 19: 1007, 20: 1007,
    21: 1007, 22: 1008, 23: 1008, 24: 1008, 25: 1009
}


class UpgradeButton(discord.ui.Button):
    def __init__(self, user, item, disabled):
        super().__init__(label=f"Upgrade!", style=discord.ButtonStyle.success, disabled=disabled)
        self.user = user
        self.item = item

    async def callback(self, interaction: discord.Interaction):
        try:
            if interaction.user.id != int(self.user.get_userId()):
                embed = discord.Embed(title=f"You're not allowed to use this action!",
                                      description="",
                                      colour=discord.Color.red())
                return await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=2)

            await interaction.response.defer()


        except discord.errors.NotFound:
            pass

class SmithingView(discord.ui.View):

    def __init__(self, user, item, disabled):
        super().__init__()
        self.user = user.update_user()
        self.add_item(UpgradeButton(user=user, item=item, disabled=disabled))


class SmithingCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="smithing", description="Upgrade your equipped weapon with materials..")
    async def smithing(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer()

            self.client.add_to_activity()

            if db.validate_user(interaction.user.id):

                user = User(interaction.user.id)

                item = user.get_weapon()
                old_level = item.get_level()
                old_dmg = item.get_total_value(user)

                new_level = item.get_level() + 1
                item.level = item.level + 1
                new_dmg = item.get_total_value(user)

                if not item:
                    embed = discord.Embed(title=f"You don't have a weapon equipped..",
                                          description="",
                                          colour=discord.Color.red())
                    return await interaction.followup.send(embed=embed, ephemeral=True)


                embed = discord.Embed(title=f"**{item.get_name()}** `+{old_level}`",
                                      description=f"Do you want to upgrade this weapon to `+{new_level}` ?")

                if item.get_icon_url() is not None and item.get_icon_url() != 'None':
                    embed.set_thumbnail(url=f"{item.get_icon_url()}")

                material_item_id = MATERIAL_TABLE[new_level]
                req_material = db.get_item_from_item_id(material_item_id)
                category_emoji = discord.utils.get(interaction.client.get_guild(763425801391308901).emojis, name="smithing_stone")
                req_material_text = f"• {category_emoji} `{req_material.get_name()}` **{new_level * 2}**x\n"

                embed.add_field(name="", value=f"**Requires Materials:** \n"
                                               f"{req_material_text}", inline=False)

                embed.add_field(name="", value=f"**After:** \n"
                                               f"`Damage:` **{old_dmg}** -> `Damage:` **{new_dmg}**", inline=False)

                embed.colour = discord.Color.orange()

                disabled = not db.has_user_enough_items(idUser=user.get_userId(), idItem=req_material.get_idItem(), reqcount=new_level * 2)
                print(disabled)
                await interaction.followup.send(embed=embed, view=SmithingView(user=user, item=item, disabled=disabled))
            else:
                await class_selection(interaction=interaction)
        except Exception as e:
            await self.client.send_error_message(e)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(SmithingCommand(client))
