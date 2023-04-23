import discord
from discord import app_commands
from discord.ext import commands

import db
from Classes.encounter import Encounter
from Classes.enemy import Enemy
from Classes.enemy_move import EnemyMove
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


class InsertEnemyMoveButton(discord.ui.Button):
    def __init__(self, user):
        super().__init__(label="Insert Enemy_Move", style=discord.ButtonStyle.success)
        self.user = user

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != int(self.user.get_userId()):
            embed = discord.Embed(title=f"You're not allowed to use this action!",
                                  description="",
                                  colour=discord.Color.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=2)

        await interaction.response.send_message(view=SelectEnemyView())


class InsertEncounterButton(discord.ui.Button):
    def __init__(self, user):
        super().__init__(label="Insert Encounter", style=discord.ButtonStyle.success)
        self.user = user

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != int(self.user.get_userId()):
            embed = discord.Embed(title=f"You're not allowed to use this action!",
                                  description="",
                                  colour=discord.Color.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=2)

        encounter = Encounter()
        preview_embed = discord.Embed(title="Add Encounter")
        preview_embed.add_field(name="Description:", value="Please enter a description..")
        preview_embed.add_field(name="Drop_rate:", value="Please enter a drop_rate..")
        preview_embed.add_field(name="Location:", value="Please select a location below")
        await interaction.response.send_message(view=SelectLocationView(embed=preview_embed, encounter=encounter), embed=preview_embed)



class ConfirmInsertButton(discord.ui.Button):
    def __init__(self, enemy: Enemy() = None, message_id: str = None, logic: str = None, location: str = None, mode = None, enemy_move: EnemyMove() = None,
                 encounter: Encounter() = None):
        super().__init__(label="Confirm", style=discord.ButtonStyle.success)
        self.enemy = enemy
        self.message_id = message_id
        self.logic = logic
        self.location = location
        self.mode = mode
        self.enemy_move = enemy_move
        self.encounter = encounter

    async def callback(self, interaction: discord.Interaction):

        guild = interaction.guild
        channel = guild.get_channel(interaction.channel_id)
        message = await channel.fetch_message(self.message_id)

        if self.mode == "enemy":
            enemy_id = int(str(db.get_enemy_count()).strip("[('',)]")) + 1
            db.add_enemy(enemy_id, db.get_enemy_logic_id_from_name(str(self.logic)), str(self.enemy.get_name()),
                         str(self.enemy.get_description()), str(self.enemy.get_health()), str(self.enemy.get_runes()),
                         str(db.get_location_id_from_name(self.location)))

            self.enemy.set_location(db.get_enemy_logic_id_from_name(self.location))
            self.enemy.set_id(str(db.get_enemy_id_from_name(self.enemy.get_name())).strip("(,)"))
            await message.edit(embed=discord.Embed(title=f"Database Insertion successful!, Enemy_id: {self.enemy.get_id()}",
                                                   colour=discord.Color.green()),
                               view=None)

        if self.mode == "enemy_move":
            db.add_enemy_move(self.enemy_move.get_description(), str(self.enemy_move.get_phase()), str(self.enemy_move.get_type()),
                              str(self.enemy.get_id()) \
                              , str(self.enemy_move.get_damage()), str(self.enemy_move.get_healing()), str(self.enemy_move.get_duration()),
                              str(self.enemy_move.get_max_targets()))
            await message.edit(
                embed=discord.Embed(title=f"Database Insertion successful!", colour=discord.Color.green()), view=None)

        if self.mode == "encounter":
            location = self.encounter.get_location()
            db.add_encounter(self.encounter.get_description(), str(self.encounter.get_drop_rate()), str(db.get_location_id_from_name(location.get_name())).strip("(,)"))
            self.encounter.set_id(db.get_encounter_id_from_description(self.encounter.get_description()))
            await message.edit(
                embed=discord.Embed(title=f"Database Insertion successful!", colour=discord.Color.green()), view=None)


class SelectEnemy(discord.ui.Select):
    def __init__(self):
        super().__init__(placeholder="Select the corresponding enemy", max_values=1, min_values=1)
        # self.enemy_id = list()
        self.enemy = None

        for enemy, desc in db.get_enemy_and_desc():
            description = str(desc).strip("'[('',)]'")
            if description == "Boss":
                self.add_option(label=str(enemy).strip("'[('',)]'"), description=description,
                                emoji="💀")
            else:
                self.add_option(label=str(enemy).strip("'[('',)]'"), description=description)

    async def callback(self, interaction: discord.Interaction):
        preview_embed = discord.Embed(title="Adding Enemy_move",
                                      description=f"The move will be added for: {str(self.values[0])}")

        self.enemy = Enemy(str(db.get_enemy_id_from_name(str(self.values[0]))).strip("(,)"))

        await interaction.message.edit(embed=preview_embed,
                                       view=SelectMoveTypeView(interaction.message.id, self.enemy, preview_embed))
        await interaction.response.defer()


class SelectEnemyLogic(discord.ui.Select):
    def __init__(self):
        super().__init__(placeholder="Select the corresponding logic", max_values=1, min_values=1)

        for logic_name in db.get_all_enemy_logic():
            self.add_option(label=str(logic_name).strip("'[('',)]'"))

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(AddEnemyModal(str(self.values[0]), str(interaction.message.id)))


class SelectMoveType(discord.ui.Select):
    def __init__(self, message_id: str, enemy: Enemy(), embed: discord.Embed):
        super().__init__(placeholder="Select the corresponding move_type", max_values=1, min_values=1)
        self.message_id = message_id
        self.enemy = enemy
        self.embed = embed

        for move_type in db.get_all_move_types():
            self.add_option(label=str(move_type).strip("'[('',)]'"))

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        channel = guild.get_channel(interaction.channel_id)
        message = await channel.fetch_message(self.message_id)
        self.embed.add_field(name="Move type:", value=str(self.values[0]))
        await message.edit(embed=self.embed, view=None)
        await interaction.response.send_modal(
            AddEnemyMoveModal(self.message_id, self.enemy, str(self.values[0]), embed=self.embed))


class SelectLocation(discord.ui.Select):
    def __init__(self, message_id: str = None, embed: discord.Embed = None, logic: str = None, enemy: Enemy() = None,
                encounter: Encounter() = None):
        super().__init__(placeholder="Select the corresponding location", max_values=1, min_values=1)
        self.enemy = enemy
        self.message_id = message_id
        self.logic = logic
        self.embed = embed
        self.encounter = encounter

        for location_name, location_description in db.get_all_locations():
            self.add_option(label=str(location_name), description=str(location_description))

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        channel = guild.get_channel(interaction.channel_id)

        if self.enemy:
            message = await channel.fetch_message(self.message_id)
            self.embed.set_field_at(index=4, name="Location:", value=str(self.values[0]))
            await interaction.response.defer()
            await message.edit(view=ConfirmInsertButtonView(self.enemy, self.message_id, self.logic, self.values[0], "enemy"),
                               embed=self.embed)

        elif self.encounter:
            self.encounter.set_location(int(str(db.get_location_id_from_name(str(self.values[0]))).strip("(,)")))
            self.embed.set_field_at(index=2, name="Location:", value=str(self.values[0]))
            await interaction.message.edit(embed=self.embed, view=None)
            await interaction.response.send_modal(AddEncounterModal(interaction.message.id, self.values[0], self.embed, encounter=self.encounter))


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
        enemy = Enemy()
        enemy.set_name(self.enemy_name)
        enemy.set_description(self.enemy_description)
        enemy.set_health(self.enemy_health)
        enemy.set_runes(self.enemy_runes)
        message = await channel.fetch_message(self.message_id)

        preview_embed = discord.Embed(title="Adding Enemy")
        preview_embed.add_field(name="Enemy name:", value=self.enemy_name)
        preview_embed.add_field(name="Enemy description:", value=self.enemy_description)
        preview_embed.add_field(name="Enemy health:", value=self.enemy_health)
        preview_embed.add_field(name="Enemy runes reward:", value=self.enemy_runes)
        preview_embed.add_field(name="Location:", value="Please select below..")

        await message.edit(embed=preview_embed,
                           view=SelectLocationView(self.message_id, preview_embed, self.logic, enemy))
        await interaction.response.defer()


class AddEnemyMoveModal(discord.ui.Modal):
    move_description = discord.ui.TextInput(label="Description", style=discord.TextStyle.long,
                                            placeholder="Enter a valid description..", required=True)
    move_phase = discord.ui.TextInput(label="Phase", style=discord.TextStyle.short,
                                      placeholder="Enter a valid phase number..", required=True)
    move_damage = None
    move_healing = None
    move_max_targets = None

    def __init__(self, message_id: str, enemy: Enemy(), move_type: str, embed: discord.Embed):
        super().__init__(title=f"Add Enemy_moves to [{enemy.get_name()}]")
        self.message_id = message_id
        self.enemy = enemy
        self.move_type = move_type
        self.embed = embed

        match move_type:
            case 'attack':
                self.move_damage = discord.ui.TextInput(label="Damage", style=discord.TextStyle.short,
                                                        placeholder="Enter a damage amount, leave empty if None..",
                                                        required=False)
                self.move_max_targets = discord.ui.TextInput(label="Max_targets", style=discord.TextStyle.short,
                                                             placeholder="Enter a valid Max_targets amount",
                                                             required=True)
                self.add_item(self.move_damage)
                self.add_item(self.move_max_targets)

            case 'heal':
                self.move_healing = discord.ui.TextInput(label="Healing", style=discord.TextStyle.short,
                                                         placeholder="Enter a healing amount, leave empty if None..",
                                                         required=False)
                self.add_item(self.move_healing)

    async def on_submit(self, interaction: discord.Interaction):

        guild = interaction.guild
        channel = guild.get_channel(interaction.channel_id)

        move = EnemyMove()
        self.embed.add_field(name="Move_description:", value=self.move_description)
        move.set_description(self.move_description)
        move.set_type(str(db.get_move_type_id_from_name(self.move_type)).strip("(,)"))

        if self.move_max_targets is None:
            move.set_max_targets(1)
        else:
            move.set_max_targets(self.move_max_targets)

        self.embed.add_field(name="Move_max_targets:", value=move.get_max_targets())

        if self.move_phase is not None:
            self.embed.add_field(name="Move_phase:", value=self.move_phase)
            move.set_phase(self.move_phase)

        if self.move_damage is not None:
            self.embed.add_field(name="Move_damage:", value=self.move_damage)
            move.set_damage(self.move_damage)
        else:
            move.set_damage(0)

        if self.move_healing is not None:
            self.embed.add_field(name="Move_healing:", value=self.move_healing)
            move.set_healing(self.move_healing)
        else:
            move.set_healing(0)

        move.set_duration(0)

        message = await channel.fetch_message(self.message_id)

        await message.edit(embed=self.embed, view=ConfirmInsertButtonView(self.enemy, self.message_id, None, None, "enemy_move", move))
        await interaction.response.defer()


class AddEncounterModal(discord.ui.Modal):
    def __init__(self, message_id: str = None, location: str = None, embed: discord.Embed = None, encounter: Encounter() = None):
        super().__init__(title="Add Encounter")
        self.message_id = message_id
        self.location = location
        self.embed = embed
        self.encounter = encounter

    encounter_description = discord.ui.TextInput(label="Description", style=discord.TextStyle.long,
                                                 placeholder="Enter a valid description..", required=True)
    encounter_dropRate = discord.ui.TextInput(label="Drop_rate", style=discord.TextStyle.short,
                                              placeholder="Enter a valid drop_rate amount..", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        self.embed.set_field_at(index=0, name="Description:", value=self.encounter_description)
        self.embed.set_field_at(index=1, name="Drop_rate:", value=self.encounter_dropRate)


        self.encounter.set_description(self.encounter_description)
        self.encounter.set_drop_rate(self.encounter_dropRate)

        await interaction.message.edit(embed=self.embed, view=ConfirmInsertButtonView(message_id=interaction.message.id, location=self.location, mode="encounter", encounter=self.encounter))
        await interaction.response.defer()

class SelectEnemyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(SelectEnemy())


class SelectELView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(SelectEnemyLogic())


class SelectMoveTypeView(discord.ui.View):
    def __init__(self, message_id: str, enemy_list: Enemy(), embed: discord.Embed):
        super().__init__(timeout=None)
        self.add_item(SelectMoveType(message_id, enemy_list, embed))


class SelectLocationView(discord.ui.View):
    def __init__(self, message_id: str = None, embed: discord.Embed = None, logic: str = None, enemy: Enemy() = None,
                 encounter: Encounter() = None):
        super().__init__(timeout=None)
        self.add_item(SelectLocation(message_id, embed, logic, enemy, encounter))


class ConfirmInsertButtonView(discord.ui.View):
    def __init__(self, enemy: Enemy() = None, message_id: str = None, logic: str = None, location: str = None, mode = None,
                 enemy_move: EnemyMove() = None, encounter: Encounter() = None):
        super().__init__(timeout=None)
        self.add_item(ConfirmInsertButton(enemy, message_id, logic, location, mode, enemy_move, encounter))


class DeveloperView(discord.ui.View):

    def __init__(self, user):
        super().__init__()
        self.user = user.update_user()
        self.add_item(CompleteQuestButton(user=user))
        self.add_item(InsertEnemyButton(user=user))
        self.add_item(InsertEnemyMoveButton(user=user))
        self.add_item(InsertEncounterButton(user=user))


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
