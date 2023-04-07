import discord
from discord import app_commands
from discord.ext import commands

import db
from Classes.enemy import Enemy
from Classes.user import User
from Utils import utils

MAX_USERS = 3


async def update_boss_fight_battle_view(enemy, users, interaction, turn_index):
    # get move from enemy
    enemy_phase = enemy.get_phase()
    enemy_move = enemy.get_move(phase=enemy_phase)
    enemy, users = enemy_move.execute(enemy=enemy, users=users)

    turn_index = cycle_turn_index(turn_index=turn_index, users=users)

    embed = discord.Embed(title=f"**Fight against `{enemy.get_name()}`**",
                          description=f"`{enemy.get_name()}`\n"
                                      f"{utils.create_health_bar(enemy.get_health(), enemy.get_max_health())} `{enemy.get_health()}/{enemy.get_max_health()}`")

    embed.add_field(name="Enemy action:", value=f"{enemy_move.get_description()}", inline=False)

    embed.add_field(name="Turn order:", value=f"**{users[turn_index].get_userName()}** please choose an action..",
                    inline=False)

    for user in users:
        embed.add_field(name=f"**`{user.get_userName()}`**",
                        value=f"{utils.create_health_bar(user.get_health(), user.get_max_health())} `{user.get_health()}/{user.get_max_health()}`",
                        inline=False)

    # Check for fight end
    if enemy.get_health() <= 0:
        # Enemy died
        embed.set_field_at(0, name="Enemy action:", value=f"**{enemy.get_name()}** has been *defeated!*", inline=False)
        embed.set_field_at(1, name="", value="", inline=False)

        await interaction.message.edit(embed=embed)
        return
    if len([user for user in users if user.get_health() > 0]) == 0:
        # All users died
        await interaction.message.edit(embed=embed)
        return

    await interaction.message.edit(embed=embed, view=BossFightBattleView(users=users, enemy=enemy, turn_index=turn_index))


def cycle_turn_index(turn_index, users):
    party_length = len(users)

    next_index = (turn_index + 1) % party_length
    while users[next_index].get_health() <= 0:
        next_index = (next_index + 1) % party_length
        if next_index == turn_index:
            # Cycle goes back to the original, everyone else died.
            return turn_index

    # Switched turns!

    return next_index


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

        await interaction.message.edit(embed=edited_embed)


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

        await update_boss_fight_battle_view(enemy=self.enemy, users=self.users, interaction=interaction,
                                            turn_index=0)  # turn_index = 0 because the first player should start the turn


class BossFightLobbyView(discord.ui.View):
    def __init__(self, users, enemy):
        super().__init__()

        disable = False
        if len(users) == MAX_USERS:
            disable = True

        self.add_item(StartButton(users=users, enemy=enemy))
        self.add_item(JoinButton(users=users, disabled=disable))


class BattleButton(discord.ui.Button):
    def __init__(self, current_user, users, enemy, turn_index, label, style):
        super().__init__(label=label, style=style)
        self.current_user = current_user
        self.users = users
        self.enemy = enemy
        self.turn_index = turn_index

    async def callback(self, interaction: discord.Interaction):
        if str(interaction.user.id) != self.current_user.get_userId():
            embed = discord.Embed(title=f"It's not your turn..",
                                  description="",
                                  colour=discord.Color.orange())
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        await interaction.response.defer()

        if self.current_user.get_health() > 0 and self.enemy.get_health() > 0:
            self.execute_action()

            await update_boss_fight_battle_view(enemy=self.enemy, users=self.users, interaction=interaction,
                                                turn_index=self.turn_index)

    def execute_action(self):
        pass


class AttackButton(BattleButton):
    def __init__(self, current_user, users, enemy, turn_index):
        super().__init__(current_user, users, enemy, turn_index, label=f"Attack ({current_user.get_damage()})",
                         style=discord.ButtonStyle.danger)

    def execute_action(self):
        self.enemy.reduce_health(self.current_user.get_damage())


class HealButton(BattleButton):
    def __init__(self, current_user, users, enemy, turn_index):
        super().__init__(current_user, users, enemy, turn_index, label=f"Heal (400)", style=discord.ButtonStyle.success)

    def execute_action(self):
        self.current_user.increase_health(400)


class BossFightBattleView(discord.ui.View):
    def __init__(self, users, enemy, turn_index):
        super().__init__()
        self.users = users
        self.enemy = enemy

        self.add_item(AttackButton(current_user=users[turn_index], users=users, enemy=enemy, turn_index=turn_index))
        self.add_item(HealButton(current_user=users[turn_index], users=users, enemy=enemy, turn_index=turn_index))


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

        embed.add_field(name=f"Enemy: **{enemy.get_name()}**", value="")
        embed.add_field(name=f"Players: **1/{MAX_USERS}**", value="", inline=False)
        embed.set_footer(text="Click the button below in order to join!")

        await interaction.response.send_message(embed=embed, view=BossFightLobbyView(users=[user], enemy=enemy))


async def setup(client: commands.Bot) -> None:
    await client.add_cog(BossFight(client), guild=discord.Object(id=763425801391308901))
