import discord
from discord import app_commands
from discord.ext import commands

import db
from Classes.user import User
from Classes.enemy import Enemy
from Utils import utils

MAX_USERS = 3

class JoinButton(discord.ui.Button):
    def __init__(self, users, disabled=False):
        super().__init__(label='Join Fight', style=discord.ButtonStyle.secondary, disabled=disabled)
        self.users = users
    async def callback(self, interaction: discord.Interaction):
        db.validate_user(interaction.user.id, interaction.user.name)
        interaction_user = User(interaction.user.id)

        if any(user.get_userId() == interaction_user.get_userId() for user in self.users):
            embed = discord.Embed(title=f"You're already taking part in this fight..",
                                  description="",
                                  colour=discord.Color.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        await interaction.response.defer()

        self.users.append(interaction_user)

        message = interaction.message
        edited_embed = message.embeds[0]
        edited_embed.set_field_at(index=1, name=f"Players: **{len(self.users)}/{MAX_USERS}**", value="", inline=False)

        await interaction.message.edit(embed=edited_embed, view=BossFightLobbyView(users=self.users))

class StartButton(discord.ui.Button):
    def __init__(self, users, enemy):
        super().__init__(label='Start!', style=discord.ButtonStyle.primary)
        self.users = users
        self.enemy = enemy

    async def callback(self, interaction: discord.Interaction):
        if str(interaction.user.id) != self.users[0].get_userId():
            embed = discord.Embed(title=f"You're not allowed to start the fight.",
                                  description="",
                                  colour=discord.Color.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        await interaction.response.defer()



        embed = discord.Embed(title=f"**Fight against `{self.enemy.get_name()}`**",
                              description=f"`{self.enemy.get_name()}`\n"
                                          f"{utils.create_health_bar(self.enemy.get_health(), self.enemy.get_max_health())} `{self.enemy.get_health()}/{self.enemy.get_max_health()}`")

        embed.add_field(name="", value=f"Monster is about to attack!\n"
                                       f"__Affected players:__\n"
                                       f"**Janik** with `-120` **damage**!",
                        inline=False)

        for user in self.users:
            embed.add_field(name=f"**`{user.get_userName()}`**", value=f"{utils.create_health_bar(user.get_health(), user.get_max_health())} `{user.get_health()}/{user.get_max_health()}`", inline=False)


        await interaction.message.edit(embed=embed, view=BossFightBattleView(users=self.users, enemy=self.enemy))

class BossFightLobbyView(discord.ui.View):
    def __init__(self, users, enemy):
        super().__init__()

        disable = False
        if len(users) == MAX_USERS:
            disable = True

        self.add_item(StartButton(users=users, enemy=enemy))
        self.add_item(JoinButton(users=users, disabled=disable))


class AttackButton(discord.ui.Button):
    def __init__(self, current_user):
        super().__init__(label=f"Attack (500)", style=discord.ButtonStyle.danger)
        self.current_user = current_user

    async def callback(self, interaction: discord.Interaction):
        if str(interaction.user.id) != self.current_user.get_userId():
            embed = discord.Embed(title=f"It's not your turn..",
                                  description="",
                                  colour=discord.Color.orange())
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        await interaction.response.defer()

        print("Attack!")

class BossFightBattleView(discord.ui.View):
    def __init__(self, users, enemy):
        super().__init__()
        self.users = users
        self.enemy = enemy
        self.add_item(AttackButton(current_user=users[0]))

class BossFight(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="startboss", description="Start a boss fight!")
    @app_commands.choices(choices=[
        app_commands.Choice(name="Public", value="public"),
        app_commands.Choice(name="Private", value="private"),
    ])
    async def startboss(self, interaction: discord.Interaction, choices: app_commands.Choice[str]):
        db.validate_user(interaction.user.id, interaction.user.name)
        user = User(interaction.user.id)
        selected_choice = choices.value

        enemy = Enemy(idEnemy=1)

        embed = discord.Embed(title=f" {user.get_userName()} is starting a {selected_choice} boss fight!",
                              description="",
                              colour=discord.Color.orange())

        embed.add_field(name=f"Enemy: **{enemy.get_name()}**",value="")
        embed.add_field(name=f"Players: **1/{MAX_USERS}**", value="", inline=False)
        embed.set_footer(text="Click the button below in order to join!")

        await interaction.response.send_message(embed=embed, view=BossFightLobbyView(users=[user], enemy=enemy))

async def setup(client:commands.Bot) -> None:
    await client.add_cog(BossFight(client), guild=discord.Object(id=763425801391308901))
