import discord
from discord import app_commands
from discord.ext import commands

import db
from Classes.user import User
from Utils.classes import class_selection


class UnEquipButton(discord.ui.Button):
    def __init__(self, user, item):
        super().__init__(label='Unequip', style=discord.ButtonStyle.success)
        self.user = user
        self.item = item

    async def callback(self, interaction: discord.Interaction):

        if interaction.user.id != int(self.user.get_userId()):
            embed = discord.Embed(title=f"You're not allowed to use this action!",
                                  description="",
                                  colour=discord.Color.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=2)

        await interaction.response.defer()

        message = interaction.message
        edited_embed = message.embeds[0]
        edited_embed.colour = discord.Color.green()
        edited_embed.set_footer(text="Successfully unequipped!")

        db.unequip(idUser=self.user.get_userId(), item=self.item)

        await interaction.message.edit(embed=edited_embed, view=None, delete_after=2)


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
        if not interaction or interaction.is_expired():
            return

        try:
            await interaction.response.defer()

            self.client.add_to_activity()

            if db.validate_user(interaction.user.id):

                user = User(interaction.user.id)
                selected_choice = choices.value

                selected_item = None
                match selected_choice:
                    case 'weapon':
                        selected_item = user.get_weapon()
                    case 'head':
                        selected_item = user.get_head()
                    case 'chest':
                        selected_item = user.get_chest()
                    case 'gauntlet':
                        selected_item = user.get_gauntlet()
                    case 'legs':
                        selected_item = user.get_legs()

                has_equipped = selected_item

                if has_equipped:
                    embed = discord.Embed(title=f"**{selected_item.get_name()}** `id: {selected_item.get_idRel()}`",
                                          description=f"Do you want to unequip this item?",
                                          colour=discord.Color.orange())

                    if selected_item.get_icon_url() is not None and selected_item.get_icon_url() != 'None':
                        embed.set_thumbnail(url=f"{selected_item.get_icon_url()}")

                    value_name = str()

                    match selected_item.get_item_type():
                        case 'Weapon':
                            value_name = "Damage"
                        case 'Armor':
                            value_name = "Armor"

                    embed.add_field(name='', value=f"**Statistics:** \n"
                                                   f"`{value_name}:` **{selected_item.get_total_value(user=user)}** `Weight:` **{selected_item.get_weight()}**")

                    await interaction.followup.send(embed=embed, view=UnEquipView(user=user, item=selected_item))
                else:
                    embed = discord.Embed(title=f"You don't have an item equipped in that category right now.",
                                          description="",
                                          colour=discord.Color.red())
                    return await interaction.followup.send(embed=embed, ephemeral=True)
            else:
                await class_selection(interaction=interaction)
        except Exception as e:
            await self.client.send_error_message(e)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(UnEquip(client))
