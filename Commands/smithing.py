import discord
from discord import app_commands
from discord.ext import commands

import db
from Classes.user import User
from Utils.classes import class_selection


MATERIAL_TABLE = {
    1: 1001, 2: 1001, 3: 1001, 4: 1002, 5: 1002, 6: 1002, 7: 1003, 8: 1003, 9: 1003, 10: 1004,
    11: 1004, 12: 1004, 13: 1005, 14: 1005, 15: 1005, 16: 1006, 17: 1006, 18: 1006, 19: 1007, 20: 1007,
    21: 1007, 22: 1008, 23: 1008, 24: 1008, 25: 1009, 26: 99999
}

async def update_item(interaction, user, edit):
    user = user.update_user()
    weapon = user.get_weapon()

    if not weapon:
        embed = discord.Embed(title=f"You don't have a weapon equipped..",
                              description="Equip one with `/equip`",
                              colour=discord.Color.red())
        return await interaction.followup.send(embed=embed, ephemeral=True)

    item = db.get_item_from_user_with_id_rel(idRel=weapon.get_idRel(), idUser=user.get_userId())

    if not item:
        embed = discord.Embed(title=f"You don't have a weapon equipped..",
                              description="",
                              colour=discord.Color.red())
        return await interaction.followup.send(embed=embed, ephemeral=True)

    old_level = item.get_level()
    old_dmg = item.get_total_value(user)
    old_scl_text = item.get_scaling_text()

    new_level = item.get_level() + 1
    item.level = item.level + 1
    new_dmg = item.get_total_value(user)
    new_scl_text = item.get_scaling_text()

    embed = discord.Embed(title=f"**{item.get_name()}** `+{old_level}`",
                          description=f"Do you want to upgrade this weapon to `+{new_level}` ?")

    if item.get_icon_url() is not None and item.get_icon_url() != 'None':
        embed.set_thumbnail(url=f"{item.get_icon_url()}")

    material_item_id = MATERIAL_TABLE[new_level]

    req_material = db.get_item_from_item_id(material_item_id)

    if not req_material:
        embed.add_field(name="Error", value="There was an error with your upgrade.. I couldn't find the required material. Please use `/feedback`.", inline=False)
        return await interaction.message.edit(embed=embed, view=None)

    # Calculate the req material count
    reqCount = 2 + (new_level % 3) * 2
    req_material.set_count(reqCount)

    category_emoji = discord.utils.get(interaction.client.get_guild(763425801391308901).emojis, name="smithing_stone")

    # Get user material count for UI and disable check
    material_count = db.get_item_count_from_user(idUser=user.get_userId(), idItem=req_material.get_idItem())

    req_material_text = f"• {category_emoji} `{req_material.get_name()}` {material_count}/**{req_material.get_count()}**\n"

    # Check if we disable the button
    disabled = material_count < req_material.get_count()

    embed.add_field(name="", value=f"**Requires Materials:** \n"
                                   f"{req_material_text}", inline=False)

    embed.add_field(name="", value=f"**After:** \n"
                                   f"`Damage:` **{old_dmg}** -> `Damage:` **{new_dmg}**", inline=False)
    embed.add_field(name="", value=f"**Scaling:** \n"
                                   f"{old_scl_text} -> {new_scl_text}")

    embed.colour = discord.Color.orange()

    if edit:
        await interaction.message.edit(embed=embed, view=SmithingView(user=user, item=item, disabled=disabled, req_material=req_material))
    else:
        await interaction.followup.send(embed=embed, view=SmithingView(user=user, item=item, disabled=disabled, req_material=req_material))

class UpgradeButton(discord.ui.Button):
    def __init__(self, user, item, disabled, req_material):
        super().__init__(label=f"Upgrade!", style=discord.ButtonStyle.success, disabled=disabled)
        self.user = user
        self.item = item
        self.req_material = req_material

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

            real_item = db.get_item_from_user_with_id_rel(idUser=self.user.get_userId(), idRel=self.item.get_idRel())
            # check if item even exists anymore
            if not real_item:
                edited_embed.colour = discord.Color.red()
                edited_embed.set_footer(text="This item no longer exists..")
                return await interaction.message.edit(embed=edited_embed, view=None)

            material_count = db.get_item_count_from_user(idUser=self.user.get_userId(), idItem=self.req_material.get_idItem())

            # Check if the user really has enough materials and that didn't change
            if material_count < self.req_material.get_count():
                edited_embed.colour = discord.Color.red()
                edited_embed.set_footer(text="You don't have enough materials anymore..")
                return await interaction.message.edit(embed=edited_embed, view=None)

            mat_idRel = db.get_idRel_from_user_with_item_id(idUser=self.user.get_userId(), idItem=self.req_material.get_idItem())

            if not mat_idRel:
                edited_embed.colour = discord.Color.red()
                edited_embed.set_footer(text="You don't have enough materials anymore..")
                return await interaction.message.edit(embed=edited_embed, view=None)

            db.decrease_item_from_user(idUser=self.user.get_userId(), relId=mat_idRel, amount=self.req_material.get_count())

            item_count = real_item.get_count()

            # check item count
            if item_count == 1:
                # item count is simply 1
                real_item.level += 1
                existing_item = db.does_item_exist_for_user(idUser=self.user.get_userId(), item=real_item)

                # +1 that item if no identical rel's exist
                if not existing_item:
                    db.update_item_from_user(idUser=self.user.get_userId(), item=real_item)

                    await update_item(interaction=interaction, user=self.user, edit=True)
                else:
                    # remove that item
                    db.decrease_item_from_user(idUser=self.user.get_userId(), relId=real_item.get_idRel(), amount=1)
                    # and increase count of identical rel
                    existing_item.count = 1
                    db.add_item_to_user(idUser=self.user.get_userId(), item=existing_item)
                    # equip that rel ID where we increased count
                    db.equip_item(idUser=self.user.get_userId(), item=existing_item)
                    await update_item(interaction=interaction, user=self.user, edit=True)
            else:
                # item count is greater than 1

                real_item.level += 1
                existing_item = db.does_item_exist_for_user(idUser=self.user.get_userId(), item=real_item)

                # check if identical +1 rel exist
                if not existing_item:
                    # reduce count from old rel
                    db.decrease_item_from_user(idUser=self.user.get_userId(), relId=real_item.get_idRel(), amount=1)
                    # create new item
                    real_item.count = 1
                    new_id_rel = db.add_item_to_user(idUser=self.user.get_userId(), item=real_item)
                    real_item.set_idRel(new_id_rel)
                    # equip that
                    db.equip_item(idUser=self.user.get_userId(), item=real_item)
                    await update_item(interaction=interaction, user=self.user, edit=True)
                else:
                    # reduce count from old rel and increase count in new rel
                    db.decrease_item_from_user(idUser=self.user.get_userId(), relId=real_item.get_idRel(), amount=1)
                    existing_item.count = 1
                    db.add_item_to_user(idUser=self.user.get_userId(), item=existing_item)
                    # equip that new rel
                    db.equip_item(idUser=self.user.get_userId(), item=existing_item)
                    await update_item(interaction=interaction, user=self.user, edit=True)

        except discord.errors.NotFound:
            pass

class SmithingView(discord.ui.View):

    def __init__(self, user, item, disabled, req_material):
        super().__init__()
        self.user = user.update_user()
        self.add_item(UpgradeButton(user=user, item=item, disabled=disabled, req_material=req_material))


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

                await update_item(interaction=interaction, user=user, edit=False)
            else:
                await class_selection(interaction=interaction)
        except Exception as e:
            await self.client.send_error_message(e)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(SmithingCommand(client))
