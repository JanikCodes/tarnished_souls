import discord
from discord import app_commands
from discord.ext import commands

import db
from Classes.user import User
from Utils.classes import class_selection


class CompleteQuestButton(discord.ui.Button):
    def __init__(self, user):
        super().__init__(label="Complete Quest", style=discord.ButtonStyle.success)
        self.user = user

    async def callback(self, interaction: discord.Interaction):

        if interaction.user.id != int(self.user.get_userId()):
            embed = discord.Embed(title=f"You're not allowed to use this action!",
                                  description="",
                                  colour=discord.Color.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=2)

        await interaction.response.defer()

        db.complete_quest(user=self.user)


class InsertEnemyButton(discord.ui.Button):
    def __init__(self, user):
        super().__init__(label="Insert Enemy", style=discord.ButtonStyle.success)
        self.user = user

    async def callback(self, interaction: discord.Interaction):

        if interaction.user.id != int(self.user.get_userId()):
            embed = discord.Embed(title=f"You're not allowed to use this action!",
                                  description="",
                                  colour=discord.Color.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=2)

        await interaction.response.send_message(view=SelectELView())


class SelectEnemyLogic(discord.ui.Select):
    def __init__(self):
        super().__init__(placeholder="Select the corresponding logic", max_values=1, min_values=1)

        for logic_name in db.get_enemy_logic():
            self.add_option(label=str(logic_name).strip("'[('',)]'"))

    async def callback(self, interaction: discord.Interaction):

        await interaction.response.send_modal(AddEnemyModal(str(self.values[0]), str(interaction.message.id)))


class SelectLocation(discord.ui.Select):
    def __init__(self, enemy: list(), message_id: str, logic: str, embed: discord.Embed):
        super().__init__(placeholder="Select the corresponding location", max_values=1, min_values=1)
        self.enemy = enemy
        self.message_id = message_id
        self.logic = logic
        self.embed = embed

        for location_name, location_description in db.get_location():
            self.add_option(label=str(location_name), description=str(location_description))

    async def callback(self, interaction: discord.Interaction):

        guild = interaction.guild
        channel = guild.get_channel(interaction.channel_id)
        message = await channel.fetch_message(self.message_id)
        self.embed.set_field_at(index=4, name="Location:", value=str(self.values[0]))
        await message.edit(view=None, embed=self.embed)


class AddEnemyModal(discord.ui.Modal):
    def __init__(self, logic, message_id):
        super().__init__(title=f"Add Enemy with [{logic}]-logic")
        self.logic = logic
        self.message_id = message_id

    enemy_name = discord.ui.TextInput(label="Name", style=discord.TextStyle.short,
                                      placeholder="Enter a valid enemy name..", required=True)
    enemy_description = discord.ui.TextInput(label="Description", style=discord.TextStyle.long,
                                             placeholder="Enter a valid enemy description..", required=True)
    enemy_health = discord.ui.TextInput(label="Health", style=discord.TextStyle.short,
                                        placeholder="Enter a valid health amount..", required=True)
    enemy_runes = discord.ui.TextInput(label="Runes", style=discord.TextStyle.short,
                                       placeholder="Enter a valid rune amount..", required=True)

    async def on_submit(self, interaction: discord.Interaction):

        guild = interaction.guild
        channel = guild.get_channel(interaction.channel_id)
        enemy = list()
        enemy.append(self.enemy_name)
        enemy.append(self.enemy_description)
        enemy.append(self.enemy_health)
        enemy.append(self.enemy_runes)
        message = await channel.fetch_message(self.message_id)

        preview_embed = discord.Embed(title="Adding Enemy")
        preview_embed.add_field(name="Enemy name:", value=self.enemy_name)
        preview_embed.add_field(name="Enemy description:", value=self.enemy_description)
        preview_embed.add_field(name="Enemy health:", value=self.enemy_health)
        preview_embed.add_field(name="Enemy runes reward:", value=self.enemy_runes)
        preview_embed.add_field(name="Location:", value="Please select below..")

        await message.edit(embed=preview_embed, view=SelectLocationView(enemy, self.message_id, self.logic, embed=preview_embed))
        await interaction.response.defer()


class SelectELView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(SelectEnemyLogic())


class SelectLocationView(discord.ui.View):
    def __init__(self, enemy: list(), message_id: str, logic: str, embed: discord.Embed):
        super().__init__(timeout=None)
        self.add_item(SelectLocation(enemy, message_id, logic, embed))


class DeveloperView(discord.ui.View):

    def __init__(self, user):
        super().__init__()
        self.user = user.update_user()
        self.add_item(CompleteQuestButton(user=user))
        self.add_item(InsertEnemyButton(user=user))


class Developer(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="developer", description="Developer only.. sorry")
    async def developer(self, interaction: discord.Interaction):
        try:
            if db.validate_user(interaction.user.id):
                user = User(interaction.user.id)

                if interaction.user.id == 321649314382348288 or interaction.user.id == 348781333839085569:

                    embed = discord.Embed(title=f"Developer options",
                                          description="What do you want to do next?")

                    await interaction.response.send_message(embed=embed, view=DeveloperView(user=user))
                else:
                    await interaction.response.send_message("You're not a developer!", ephemeral=True)
            else:
                await class_selection(interaction=interaction)
        except Exception as e:
            await self.client.send_error_message(e)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Developer(client))
