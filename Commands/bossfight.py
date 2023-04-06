import discord
from discord import app_commands
from discord.ext import commands

import db
from Classes.user import User

MAX_USERS = 3

class JoinButton(discord.ui.Button):
    def __init__(self,leader_user, users, disabled=False):
        super().__init__(label='Join Fight', style=discord.ButtonStyle.secondary, disabled=disabled)
        self.leader_user = leader_user
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

        print("User joined fight!")
        self.users.append(interaction_user)

        message = interaction.message
        edited_embed = message.embeds[0]
        edited_embed.set_field_at(index=0, name="Players:", value=f"{len(self.users)}/{MAX_USERS}")

        await interaction.message.edit(embed=edited_embed, view=BossFightView(leader_user=self.leader_user, users=self.users))

class StartButton(discord.ui.Button):
    def __init__(self, leader_user):
        super().__init__(label='Start!', style=discord.ButtonStyle.primary)
        self.leader_user = leader_user

    async def callback(self, interaction: discord.Interaction):
        if str(interaction.user.id) != self.leader_user.get_userId():
            print(f"{interaction.user.id} == {self.leader_user.get_userId()}")
            embed = discord.Embed(title=f"You're not allowed to start the fight.",
                                  description="",
                                  colour=discord.Color.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        await interaction.response.defer()

        print("Starting bossfight!")

class BossFightView(discord.ui.View):
    def __init__(self, leader_user, users):
        super().__init__()
        self.leader_user = leader_user.update_user()
        self.users = users

        disable = False
        if len(users) == MAX_USERS:
            disable = True

        self.add_item(StartButton(leader_user=leader_user))
        self.add_item(JoinButton(leader_user=leader_user, users=users, disabled=disable))

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

        embed = discord.Embed(title=f" {user.get_userName()} is starting a {selected_choice} boss fight!",
                              description="",
                              colour=discord.Color.orange())
        embed.add_field(name="Players:",value=f"1/{MAX_USERS}")
        embed.set_footer(text="Click the button below in order to join!")

        await interaction.response.send_message(embed=embed, view=BossFightView(leader_user=user, users=[user]))

async def setup(client:commands.Bot) -> None:
    await client.add_cog(BossFight(client), guild=discord.Object(id=763425801391308901))
