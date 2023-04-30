import discord
from discord import app_commands
from discord.ext import commands

import config
import db
from Classes.enemy import Enemy
from Classes.user import User
from Utils import utils
from Utils.classes import class_selection

MAX_USERS = 3
STAMINA_REGEN = 7
STAMINA_COST = 45
HEAL_AMOUNT = 400

class Fight:
    def __init__(self, enemy, users, interaction, turn_index):
        self.enemy = enemy
        self.users = users
        self.interaction = interaction
        self.turn_index = turn_index

    def get_enemy(self):
        return self.enemy

    def get_users(self):
        return self.users

    def get_interaction(self):
        return self.interaction

    def get_turn_index(self):
        return self.turn_index

    def get_current_user(self):
        return self.users[self.turn_index]

    def check_phase_change(self, enemy):
        enemy_logic = enemy.get_logic()

        match enemy_logic.get_id():
            case 1:
                # none ( do nothing )
                pass
            case 2:
                # full
                if enemy.get_health() == 0:
                    enemy.set_health(enemy.get_max_health())
                    enemy.increase_phase()
            case 3:
                # half
                if enemy.get_health() <= enemy.get_max_health() / 2:
                    enemy.increase_phase()
            case _:
                raise ValueError(f"ERROR: Invalid enemy logic ID: {enemy_logic.get_id()}")


    async def update_fight_battle_view(self):
        # reset enemy dodge state
        self.enemy.reset_dodge()

        self.check_phase_change(self.enemy)

        # get move from enemy
        enemy_phase = self.enemy.get_phase()
        enemy_move = self.enemy.get_move(phase=enemy_phase)
        enemy, users = enemy_move.execute(enemy=self.enemy, users=self.users)
        self.turn_index = turn_index = self.cycle_turn_index(turn_index=self.turn_index, users=users)

        for user in users:
            user.increase_stamina(STAMINA_REGEN)
            user.reset_dodge()

        embed = discord.Embed(title=f"**Fight against `{enemy.get_name()}`**",
                              description=f"`{enemy.get_name()}`\n"
                                          f"{utils.create_health_bar(enemy.get_health(), enemy.get_max_health(), self.interaction)} `{enemy.get_health()}/{enemy.get_max_health()}` {enemy.get_last_move_text()}")

        embed.add_field(name="Enemy action:", value=f"{enemy_move.get_description()}", inline=False)

        embed.add_field(name="Turn order:", value=f"**<@{users[turn_index].get_userId()}>** please choose an action..",
                        inline=False)

        flask_emoji = discord.utils.get(self.interaction.client.get_guild(config.botConfig["hub-server-guild-id"]).emojis, name='flask')
        # create UI for every user
        for user in users:
            embed.add_field(name=f"**`{user.get_userName()}`** {flask_emoji} {user.get_remaining_flasks()}",
                            value=f"{utils.create_health_bar(user.get_health(), user.get_max_health(), self.interaction)} `{user.get_health()}/{user.get_max_health()}` {user.get_last_move_text()}\n"
                                  f"{utils.create_stamina_bar(user.get_stamina(), user.get_max_stamina(), self.interaction)} `{user.get_stamina()}/{user.get_max_stamina()}`",
                            inline=False)
            user.clear_last_move_text()

        enemy.clear_last_move_text()


        # Check for fight end
        if enemy.get_health() <= 0:
            # Enemy died

            # get random item drops from enemy
            item_drops = enemy.get_item_rewards()
            item_drop_text = str()
            for item in item_drops:
                category_emoji = discord.utils.get(self.interaction.client.get_guild(config.botConfig["hub-server-guild-id"]).emojis,
                                                   name=item.get_iconCategory())
                item_drop_text += f"Received {category_emoji} **{item.get_name()}** {item.get_count()}x \n"

            embed.set_field_at(0, name="Enemy action:", value=f"**{enemy.get_name()}** has been *defeated!*", inline=False)
            embed.set_field_at(1, name="Reward:", value=f"Received **{enemy.get_runes()}** runes!", inline=False)
            embed.set_field_at(1, name="Items:", value=item_drop_text, inline=False)

            # grant rune rewards to all players
            for user in users:
                db.increase_runes_from_user_with_id(user.get_userId(), enemy.get_runes())

                # give each user the item drops
                for item in item_drops:
                    db.add_item_to_user(user.get_userId(), item)
                    # update quest progress
                    db.check_for_quest_update(idUser=users[0].get_userId(), item=item, runes=enemy.get_runes())

            # update quest enemy progress for host
            db.check_for_quest_update(idUser=users[0].get_userId(), idEnemy=enemy.get_id())

            await self.interaction.message.edit(embed=embed, view=None)
            return
        if len([user for user in users if user.get_health() > 0]) == 0:
            # All users died
            embed.set_field_at(0, name="Enemy action:", value=f"**{enemy.get_name()}** has *defeated all players!*",
                               inline=False)
            embed.set_field_at(1, name="", value="", inline=False)

            await self.interaction.message.edit(embed=embed, view=None)
            return

        await self.interaction.message.edit(embed=embed,
                                       view=FightBattleView(fight=self))


    def cycle_turn_index(self, turn_index, users):
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
        super().__init__(label='Join Lobby', style=discord.ButtonStyle.secondary, disabled=disabled)
        self.users = users

    async def callback(self, interaction: discord.Interaction):
        if db.validate_user(interaction.user.id):
            interaction_user = User(interaction.user.id)

            if any(user.get_userId() == interaction_user.get_userId() for user in self.users):
                embed = discord.Embed(title=f"You're already taking part in this fight..",
                                      description="",
                                      colour=discord.Color.red())
                return await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=2)
            await interaction.response.defer()

            self.users.append(interaction_user)

            message = interaction.message
            edited_embed = message.embeds[0]
            edited_embed.set_field_at(index=1, name=f"Players: **{len(self.users)}/{MAX_USERS}**", value="",
                                      inline=False)

            await interaction.message.edit(embed=edited_embed)
        else:
            embed = discord.Embed(title=f"Please choose a class first",
                                  description=f"You can do that by tying any command for example `/explore` or `/character`",
                                  colour=discord.Color.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=8)

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
            return await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=2)
        await interaction.response.defer()

        health_increase = 0

        if len(self.users) > 1:
            health_increase = self.enemy.get_max_health() * ((len(self.users) - 1) * 0.15)

        self.enemy.set_max_health(self.enemy.get_max_health() + health_increase)

        fight = Fight(enemy=self.enemy, users=self.users, interaction=interaction, turn_index=0)
        await fight.update_fight_battle_view()

class FightSelectView(discord.ui.View):
    def __init__(self, users, visibility):
        super().__init__()

        self.add_item(FightEnemySelect(users=users, visibility=visibility))


class BattleButton(discord.ui.Button):
    def __init__(self, fight, label, style):
        super().__init__(label=label, style=style)
        self.fight = fight

    async def callback(self, interaction: discord.Interaction):
        if str(interaction.user.id) != self.fight.get_current_user().get_userId():
            embed = discord.Embed(title=f"It's not your turn..",
                                  description="",
                                  colour=discord.Color.orange())
            return await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=2)
        await interaction.response.defer()

        if self.fight.get_current_user().get_health() > 0 and self.fight.get_enemy().get_health() > 0:
            self.execute_action()

            await self.fight.update_fight_battle_view()

    def execute_action(self):
        pass


class InstaKillButton(BattleButton):
    def __init__(self, fight):
        super().__init__(fight, label=f"Attack (-99999)", style=discord.ButtonStyle.danger)
    def execute_action(self):
        self.fight.get_enemy().reduce_health(99999)

class AttackButton(BattleButton):
    def __init__(self, fight):
        super().__init__(fight, label=f"Attack (-{fight.get_current_user().get_damage()})",
                         style=discord.ButtonStyle.danger)

    def execute_action(self):
        if not self.fight.get_enemy().get_is_dodging():
            self.fight.get_enemy().reduce_health(self.fight.get_current_user().get_damage())


class HealButton(BattleButton):
    def __init__(self, fight):
        super().__init__(fight, label=f"Heal (+300)",
                         style=discord.ButtonStyle.success)
        # Disable button if no flasks remaining
        self.disabled = fight.get_current_user().get_remaining_flasks() == 0

    def execute_action(self):
        self.fight.get_current_user().increase_health(HEAL_AMOUNT)


class DodgeButton(BattleButton):
    def __init__(self, fight):
        super().__init__(fight, label=f"Dodge (-{STAMINA_COST})",
                         style=discord.ButtonStyle.primary)

        # Disable button if not enough stamina
        self.disabled = fight.get_current_user().get_stamina() < STAMINA_COST

    def execute_action(self):
        self.fight.get_current_user().dodge(STAMINA_COST)


class FightBattleView(discord.ui.View):
    def __init__(self, fight):
        super().__init__()

        self.add_item(AttackButton(fight=fight))
        self.add_item(HealButton(fight=fight))
        self.add_item(DodgeButton(fight=fight))
        #self.add_item(InstaKillButton(current_user=users[turn_index], users=users, enemy=enemy, turn_index=turn_index))

class FightLobbyView(discord.ui.View):
    def __init__(self, users, enemy, visibility):
        super().__init__()

        # disable join button if reached max users
        disable = False
        if len(users) == MAX_USERS:
            disable = True

        self.add_item(StartButton(users=users, enemy=enemy))
        if visibility == 'public':
            self.add_item(JoinButton(users=users, disabled=disable))

class FightEnemySelect(discord.ui.Select):
    def __init__(self, users, visibility):
        super().__init__(placeholder="Choose an enemy")
        self.users = users
        self.visibility = visibility

        for enemy in db.get_all_enemies_from_location(idLocation=users[0].get_current_location().get_id()):
            if enemy.get_description() == "Boss":
                self.add_option(label=f"{enemy.get_name()}", description=f"{enemy.get_description()}", value=f"{enemy.get_id()}", emoji="💀")
            else:
                self.add_option(label=f"{enemy.get_name()}", description=f"{enemy.get_description()}",value=f"{enemy.get_id()}")

    async def callback(self, interaction: discord.Interaction):

        if str(interaction.user.id) != self.users[0].get_userId():
            embed = discord.Embed(title=f"You're not allowed to use this action!",
                                  description="",
                                  colour=discord.Color.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=2)

        await interaction.response.defer()

        selected_enemy = Enemy(self.values[0])

        embed = discord.Embed(title=f" {self.users[0].get_userName()} has started a {self.visibility} lobby",
                              description="",
                              colour=discord.Color.orange())

        embed.add_field(name=f"Enemy: **{selected_enemy.get_name()}**", value="")
        embed.add_field(name=f"Players: **1/{MAX_USERS}**", value="", inline=False)

        if self.visibility == 'public':
            embed.set_footer(text="Click the button below in order to join!")

        await interaction.message.edit(embed=embed, view=FightLobbyView(users=self.users, enemy=selected_enemy, visibility=self.visibility))

class FightCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="fight", description="Choose an enemy to fight in your current location")
    @app_commands.choices(visibility=[
        app_commands.Choice(name="Solo", value="solo"),
        app_commands.Choice(name="Public", value="public"),
    ])
    async def fight(self, interaction: discord.Interaction, visibility: app_commands.Choice[str]):
        await interaction.response.defer()

        try:
            if db.validate_user(interaction.user.id):

                user = User(interaction.user.id)
                selected_visibility = visibility.value

                embed = discord.Embed(title=f" {user.get_userName()} is choosing an enemy to fight..",
                                      description=f"The enemies below are all from `{user.get_current_location().get_name()}`\n"
                                                  f"*You can fight different enemies if you change your location with* `/travel`",
                                      colour=discord.Color.orange())

                await interaction.followup.send(embed=embed, view=FightSelectView(users=[user], visibility=selected_visibility))
            else:
                await class_selection(interaction=interaction)
        except Exception as e:
            await self.client.send_error_message(e)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(FightCommand(client))
