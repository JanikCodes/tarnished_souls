import discord
from discord import app_commands
from discord.ext import commands

import db
from Classes.user import User
from Utils import utils
from Utils.classes import class_selection


class UpgradeStatsButton(discord.ui.Button):
    def __init__(self, text, button_style, func, selected_choice, user, disabled=False):
        super().__init__(label=text, style=button_style, disabled=disabled)
        self.func = func
        self.selected_choice = selected_choice
        self.user = user

    async def callback(self, interaction: discord.Interaction):

        if interaction.user.id != int(self.user.get_userId()):
            embed = discord.Embed(title=f"You're not allowed to use this action!",
                                  description="",
                                  colour=discord.Color.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        await interaction.response.defer()

        if self.func == "upgrade":
            runes_cost = utils.calculate_upgrade_cost(user=self.user, next_upgrade_cost=True)

            if self.user.get_runes() >= runes_cost:
                db.increase_stat_from_user_with_id(userId=self.user.get_userId(), stat_name=self.selected_choice)
                db.decrease_runes_from_user_with_id(userId=self.user.get_userId(), amount=runes_cost)
                current_level = db.get_stat_level_from_user_with_id(userId=self.user.get_userId(),
                                                                    value=self.selected_choice)
                message = interaction.message
                edited_embed = message.embeds[0]
                edited_embed.set_field_at(0, name=f"**{self.selected_choice}**",
                                          value=utils.create_bars(current_level, 100) + utils.create_invisible_spaces(
                                              3) + str(current_level) + "/100", inline=False)

                await interaction.message.edit(embed=edited_embed,
                                               view=UpgradeStatsView(current_level=current_level, user=self.user,
                                                                     selected_choice=self.selected_choice,
                                                                     next_upgrade_cost=False))


class UpgradeStatsView(discord.ui.View):

    def __init__(self, user, current_level, selected_choice, next_upgrade_cost):
        super().__init__()
        self.user = user.update_user()
        self.current_level = current_level
        disabled = True if utils.calculate_upgrade_cost(user=self.user,
                                                        next_upgrade_cost=next_upgrade_cost) > user.get_runes() else False
        self.add_item(UpgradeStatsButton(
            f"Upgrade for {utils.calculate_upgrade_cost(user=self.user, next_upgrade_cost=next_upgrade_cost)} runes",
            discord.ButtonStyle.success, "upgrade", selected_choice, user, disabled=disabled))
        self.add_item(UpgradeStatsButton(f"{self.user.get_runes()} runes", discord.ButtonStyle.grey, "soul-display",
                                         selected_choice, user, True))


class UpgradeStats(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="upgrade", description="Upgrade one of your available stats")
    @app_commands.choices(choices=[
        app_commands.Choice(name="Vigor", value="vigor"),
        app_commands.Choice(name="Mind", value="mind"),
        app_commands.Choice(name="Endurance", value="endurance"),
        app_commands.Choice(name="Strength", value="strength"),
        app_commands.Choice(name="Dexterity", value="dexterity"),
        app_commands.Choice(name="Intelligence", value="intelligence"),
        app_commands.Choice(name="Faith", value="faith"),
        app_commands.Choice(name="Arcane", value="arcane"),
    ])
    async def upgrade_stats(self, interaction: discord.Interaction, choices: app_commands.Choice[str]):
        if db.validate_user(interaction.user.id):
            user = User(interaction.user.id)
            selected_choice = choices.value
            current_level = db.get_stat_level_from_user_with_id(user.get_userId(), selected_choice)

            embed = discord.Embed(title=f"**Upgrade {selected_choice}**",
                                  description=f"Click the button below to upgrade your skill!")
            embed.set_author(name=user.get_userName())
            embed.add_field(name=f"**{selected_choice}**",
                            value=utils.create_bars(current_level, 100) + utils.create_invisible_spaces(3) + str(
                                current_level) + "/100", inline=False)
            await interaction.response.send_message(embed=embed,
                                                    view=UpgradeStatsView(user=user, current_level=current_level,
                                                                          selected_choice=selected_choice,
                                                                          next_upgrade_cost=True))
        else:
            await class_selection(interaction=interaction)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(UpgradeStats(client), guild=discord.Object(id=763425801391308901))
