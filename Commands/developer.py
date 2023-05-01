import discord
from discord import app_commands
from discord.ext import commands

import config
import db
from Classes.encounter import Encounter
from Classes.enemy import Enemy
from Classes.enemy_logic import EnemyLogic
from Classes.enemy_move import EnemyMove
from Classes.item import Item
from Classes.quest import Quest
from Classes.user import User
from Utils.classes import class_selection
import os


class CompleteQuestButton(discord.ui.Button):
    def __init__(self, user):
        super().__init__(label="Complete Quest", style=discord.ButtonStyle.success)
        self.user = user

    async def callback(self, interaction: discord.Interaction):
        if not interaction.user.id in config.botConfig["developer-ids"]:
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
        if not interaction.user.id in config.botConfig["developer-ids"]:
            embed = discord.Embed(title=f"You're not allowed to use this action!", description="",colour=discord.Color.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=2)
        else:
            await interaction.response.send_message(view=SelectELView())


class InsertEnemyMoveButton(discord.ui.Button):
    def __init__(self, user):
        super().__init__(label="Insert Enemy_Move", style=discord.ButtonStyle.success)
        self.user = user

    async def callback(self, interaction: discord.Interaction):
        if not interaction.user.id in config.botConfig["developer-ids"]:
            embed = discord.Embed(title=f"You're not allowed to use this action!",
                                  description="",
                                  colour=discord.Color.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=2)

        await interaction.response.send_message(view=SelectEnemyLocationView())


class InsertEncounterButton(discord.ui.Button):
    def __init__(self, user):
        super().__init__(label="Insert Encounter", style=discord.ButtonStyle.success)
        self.user = user

    async def callback(self, interaction: discord.Interaction):
        if not interaction.user.id in config.botConfig["developer-ids"]:
            embed = discord.Embed(title=f"You're not allowed to use this action!",
                                  description="",
                                  colour=discord.Color.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=2)

        encounter = Encounter()
        preview_embed = discord.Embed(title="Add Encounter")
        preview_embed.add_field(name="Description:", value="Please enter a description..")
        preview_embed.add_field(name="Drop_rate:", value="Please enter a drop_rate..")
        preview_embed.add_field(name="Location:", value="Please select a location below")
        await interaction.response.send_message(view=SelectLocationView(embed=preview_embed, encounter=encounter),
                                                embed=preview_embed)


class InsertQuestButton(discord.ui.Button):
    def __init__(self, user):
        super().__init__(label="Insert Quest", style=discord.ButtonStyle.success)
        self.user = user

    async def callback(self, interaction: discord.Interaction):
        if not interaction.user.id in config.botConfig["developer-ids"]:
            embed = discord.Embed(title=f"You're not allowed to use this action!",
                                  description="",
                                  colour=discord.Color.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=2)

        quest = Quest()
        preview_embed = discord.Embed(title="Add Quest")
        preview_embed.add_field(name="Title:", value="Please enter a title..")
        preview_embed.add_field(name="Description:", value="Please enter a description..")
        preview_embed.add_field(name="Req_kills:", value="Please enter a req. kills amount..")
        preview_embed.add_field(name="Req_item_count:", value="Please enter a req. item count..")
        preview_embed.add_field(name="Req_runes:", value="Please enter a req. runes amount..")
        preview_embed.add_field(name="Item_id:", value="Please enter a valid item_id..")
        preview_embed.add_field(name="Enemy_id:", value="Please enter a valid enemy..")
        preview_embed.add_field(name="Rune_reward:", value="Please enter a valid rune reward amount..")
        preview_embed.add_field(name="Location_id_reward:", value="Please enter a valid location_id_reward..")
        preview_embed.add_field(name="Req_explore_count:", value="Please enter a valid req. explore_count amount..")
        preview_embed.add_field(name="Location_id:", value="Please enter a valid location_id..")
        preview_embed.add_field(name="Cooldown:", value="Please enter a valid cooldown amount..")
        preview_embed.add_field(name="Flask_reward:", value="Please enter a valid flask_amount..")
        await interaction.response.send_message(embed=preview_embed,
                                                view=SelectLocationView(quest=quest, embed=preview_embed))


class ShowSQLTXTButton(discord.ui.Button):
    def __init__(self, user):
        super().__init__(label="Show SQL.txt", style=discord.ButtonStyle.success)
        self.user = user

    async def callback(self, interaction: discord.Interaction):
        if not interaction.user.id in config.botConfig["developer-ids"]:
            embed = discord.Embed(title=f"You're not allowed to use this action!",
                                  description="",
                                  colour=discord.Color.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=2)

        if os.stat("Data/sql-statements.txt").st_size != 0:
            with open("Data/sql-statements.txt", "rb") as file:
                await interaction.response.send_message(file=discord.File(file, "sql-statements.txt"))
        else:
            await interaction.response.send_message(content="You haven't created any statements yet!", ephemeral=True, delete_after=3)


class UpdateDEVMaxLocation(discord.ui.Button):
    def __init__(self, user):
        super().__init__(label="Update maxLocation=13", style=discord.ButtonStyle.success)
        self.user = user

    async def callback(self, interaction: discord.Interaction):
        if not interaction.user.id in config.botConfig["developer-ids"]:
            embed = discord.Embed(title="You're not allowed to use this action!",
                                  description="",
                                  colour=discord.Color.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=2)

        if db.update_dev_user_maxLocation(interaction.user.id):
            await interaction.response.send_message(content="Successfully updated your maxLocation to all 13.", ephemeral=True, delete_after=3)
        else:
            await interaction.response.send_message(content=f"I wasn't able to update your maxLocation. idUser={interaction.user.id}", ephemeral=True, delete_after=2)


class ConfirmInsertButton(discord.ui.Button):
    def __init__(self, enemy: Enemy() = None, mode=None, enemy_move: EnemyMove() = None,
                 encounter: Encounter() = None, quest: Quest() = None, embed: discord.Embed() = None):
        super().__init__(label="Confirm", style=discord.ButtonStyle.success)
        self.enemy = enemy
        self.mode = mode
        self.enemy_move = enemy_move
        self.encounter = encounter
        self.quest = quest
        self.embed = embed

    async def callback(self, interaction: discord.Interaction):
        if self.mode == "enemy":
            # update with new master pull
            enemy_id = db.get_enemy_count() + 1
            self.enemy.set_id(enemy_id)
            location = self.enemy.get_location()[0]
            sql = db.add_enemy(enemy=self.enemy, location_id=location.get_id())
            embed = discord.Embed(title=f"Database Insertion successful!, Enemy_id: {self.enemy.get_id()}", colour=discord.Color.green())
            embed.set_footer(text=sql)

            with open('Data/sql-statements.txt', 'a') as f:
                f.write(f"{sql};\n")

            await interaction.message.edit(embed=embed, view=InsertEnemyHasItemView(enemy=self.enemy, mode="enemy_no_item"))

        if self.mode == "enemy_with_item":
            with open('Data/sql-statements.txt', 'a') as f:
                for item in self.enemy.get_item_rewards():
                    sql = db.add_enemy_has_item(item.get_idItem(), self.enemy.get_id(), item.get_count(), item.get_drop_rate())
                    f.write(f"{sql};\n")
            embed = discord.Embed(title=f"Database Insertion successful!", colour=discord.Color.green())
            await interaction.message.edit(embed=embed, view=None, delete_after=5)

        if self.mode == "enemy_no_item":
            await interaction.message.delete()

        if self.mode == "enemy_move":
            sql = db.add_enemy_move(self.enemy_move, self.enemy)
            embed = discord.Embed(title=f"Database Insertion successful!", colour=discord.Color.green())
            embed.set_footer(text=sql)

            with open('Data/sql-statements.txt', 'a') as f:
                f.write(f"{sql};\n")

            await interaction.message.edit(embed=embed, view=None, delete_after=5)

        if self.mode == "encounter":
            self.encounter.set_id(db.get_encounter_id_from_description(self.encounter.get_description()))
            sql = db.add_encounter(self.encounter)

            embed = discord.Embed(title=f"Database Insertion successful!", colour=discord.Color.green())
            embed.set_footer(text=sql)

            with open('Data/sql-statements.txt', 'a') as f:
                f.write(f"{sql};\n")

            await interaction.message.edit(embed=embed, view=None, delete_after=5)

        if self.mode == "quest":
            sql = db.add_quest(self.quest)
            self.quest.set_id(db.get_quest_id_from_title_and_desc(self.quest.get_title(), self.quest.get_description()))
            embed = discord.Embed(title=f"Database Insertion successful!",
                                  colour=discord.Color.green())
            embed.set_footer(text=sql)
            await interaction.message.edit(embed=embed, view=InsertQuestHasItemView(embed=embed, quest=self.quest, mode="quest_no_item"))

            with open('Data/sql-statements.txt', 'a') as f:
                f.write(f"{sql};\n")

        if self.mode == "quest_no_item":
            await interaction.message.delete()

        if self.mode == "quest_with_item":
            embed = discord.Embed(title=f"Database Insertion successful!", colour=discord.Color.green())
            await interaction.message.edit(embed=embed, view=None, delete_after=5)

            with open('Data/sql-statements.txt', 'a') as f:
                for item in self.quest.get_item_reward():
                    sql = db.add_quest_has_item(self.quest.get_id(), item.get_idItem(), item.get_count())
                    f.write(f"{sql}\n")

        await interaction.response.defer()


class InsertQuestHasItemButton(discord.ui.Button):
    def __init__(self, embed: discord.Embed = None, quest: Quest() = None):
        super().__init__(label="Insert Quest Reward", style=discord.ButtonStyle.success)
        self.embed = embed
        self.quest = quest

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(AddQuestModal(embed=self.embed, modal_page=3, quest=self.quest))


class AddEnemyItemDropButton(discord.ui.Button):
    def __init__(self, enemy: Enemy() = None, embed: discord.Embed = None):
        super().__init__(label="Add Item Drop", style=discord.ButtonStyle.success)
        self.enemy = enemy
        self.embed = embed

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(AddEnemyModal(item_drop=True, enemy=self.enemy, embed=self.embed))


class NextQuestModalButton(discord.ui.Button):
    def __init__(self, embed: discord.Embed = None, quest: Quest() = None,
                 modal_page=None):
        super().__init__(label="Next", style=discord.ButtonStyle.success)
        self.embed = embed
        self.quest = quest
        self.modal_page = modal_page

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(AddQuestModal(embed=self.embed, modal_page=self.modal_page, quest=self.quest))
        

class SelectEnemyLocation(discord.ui.Select):
    def __init__(self, quest: Quest() = None, embed: discord.Embed() = None, modal_page=None):
        super().__init__(placeholder="Select the location to display all enemies", max_values=1, min_values=1)
        self.location_id = None
        self.quest = quest
        self.embed = embed
        self.modal_page = modal_page

        for location_name, location_description, location_id in db.get_all_locations():
            self.add_option(label=location_name, description=location_description, value=location_id)

    async def callback(self, interaction: discord.Interaction):
        try:
            if self.quest:
                await interaction.message.edit(view=SelectEnemyView(quest=self.quest, embed=self.embed, modal_page=self.modal_page, location_id=self.values[0]))
            else:
                await interaction.message.edit(view=SelectEnemyView(location_id=self.values[0]))
        except:
            await interaction.message.edit(view=SelectEnemyLocationView())
            await interaction.response.send_message(content="There are no enemies in this location!", ephemeral=True, delete_after=2)
            return
        await interaction.response.defer()


class SelectEnemy(discord.ui.Select):
    def __init__(self, quest: Quest() = None, embed: discord.Embed() = None, modal_page = None, location_id = None):
        super().__init__(placeholder="Select the corresponding enemy", max_values=1, min_values=1)
        self.enemy = None
        self.quest = quest
        self.embed = embed
        self.modal_page = modal_page
        self.location_id = location_id

        for enemy in db.get_enemies_from_location(location_id=self.location_id):
            if enemy.get_description() and enemy.get_description().upper() == "BOSS":
                self.add_option(label=enemy.get_name(), description=enemy.get_description(),value=enemy.get_id(),
                                emoji="💀")
            else:
                self.add_option(label=enemy.get_name(), description=enemy.get_description(),value=enemy.get_id())


    async def callback(self, interaction: discord.Interaction):

        enemy = Enemy(self.values[0])
        if self.quest:
            self.quest.set_req_enemy(enemy.get_id())

            self.embed.set_field_at(index=6, name=f"Enemy_id: {enemy.get_id()}", value=enemy.get_name())

            await interaction.message.edit(embed=self.embed, view=ConfirmInsertButtonView(quest=self.quest, mode="quest"))
            await interaction.response.defer()
            return
        else:
            self.enemy = Enemy(idEnemy=enemy.get_id())

            preview_embed = discord.Embed(title="Adding Enemy_move", description=f"The move will be added for: {enemy.get_name()}")

            await interaction.message.edit(embed=preview_embed, view=SelectMoveTypeView(self.enemy, preview_embed))
            await interaction.response.defer()
            return


class SelectEnemyLogic(discord.ui.Select):
    def __init__(self):
        super().__init__(placeholder="Select the corresponding logic", max_values=1, min_values=1)
        for logic in db.get_all_enemy_logic():
            self.add_option(label=logic.get_name(), value=logic.get_id())

    async def callback(self, interaction: discord.Interaction):
        enemy = Enemy()
        enemy.set_logic(self.values[0])
        await interaction.response.send_modal(AddEnemyModal(enemy=enemy))


class SelectMoveType(discord.ui.Select):
    def __init__(self, enemy: Enemy(), embed: discord.Embed):
        super().__init__(placeholder="Select the corresponding move_type", max_values=1, min_values=1)
        self.enemy = enemy
        self.embed = embed

        for move_type in db.get_all_move_types():
            self.add_option(label=move_type[0])

    async def callback(self, interaction: discord.Interaction):
        self.embed.add_field(name="Move type:", value=self.values[0])
        await interaction.message.edit(embed=self.embed, view=None)
        await interaction.response.send_modal(AddEnemyMoveModal(self.enemy, self.values[0], embed=self.embed))


class SelectLocation(discord.ui.Select):
    def __init__(self, embed: discord.Embed = None, enemy: Enemy() = None,
                 encounter: Encounter() = None, quest: Quest() = None, index=None):
        if index == 2:
            super().__init__(placeholder="Select the corresponding reward_location", max_values=1, min_values=1)
        else:
            super().__init__(placeholder="Select the corresponding location", max_values=1, min_values=1)
        self.enemy = enemy
        self.embed = embed
        self.encounter = encounter
        self.quest = quest
        self.index = index

        if self.quest:
            self.add_option(label="None", description="Select for no location", value="no_location")

        for location_name, location_description, location_id in db.get_all_locations():
            self.add_option(label=location_name, description=location_description, value=location_id)

    async def callback(self, interaction: discord.Interaction):
        if self.enemy:
            self.enemy.set_location(db.get_location_from_id(self.values[0]))
            location = self.enemy.get_location()[0]

            self.embed.set_field_at(index=3, name="Location:", value=location.get_name())
            await interaction.message.edit(view=ConfirmInsertButtonView(enemy=self.enemy, mode="enemy"), embed=self.embed)

        elif self.encounter:
            self.encounter.set_location(db.get_location_from_id(self.values[0]))
            location = self.encounter.get_location()[0]

            self.embed.set_field_at(index=2, name=f"Location_id: {location.get_id()}", value=location.get_name())

            await interaction.message.edit(embed=self.embed, view=None)
            await interaction.response.send_modal(AddEncounterModal(embed=self.embed, encounter=self.encounter))
            return

        elif self.quest and self.index == 1:
            if self.values[0] == "no_location":
                self.quest.set_explore_location(None)
                self.embed.set_field_at(index=10, name=f"Location_id: None", value="no_location")
            else:
                self.quest.set_explore_location(db.get_location_from_id(self.values[0]))
                ex_loc = self.quest.get_explore_location()[0]

                self.embed.set_field_at(index=10, name=f"Location_id: {ex_loc.get_id()}", value=ex_loc.get_name())

            if not self.quest.get_location_reward() or None:
                await interaction.message.edit(embed=self.embed, view=SelectLocationView(embed=self.embed, quest=self.quest))
            else:
                await interaction.message.edit(embed=self.embed, view=None)
                await interaction.response.send_modal(AddQuestModal(modal_page=1, embed=self.embed, quest=self.quest))
                return

        elif self.quest and self.index == 2:
            if self.values[0] == "no_location":
                self.quest.set_location_reward(None)
                self.embed.set_field_at(index=8, name=f"Location_id_reward: None", value=f"no_location")
            else:
                self.quest.set_location_reward(db.get_location_from_id(self.values[0]))
                rew_loc = self.quest.get_location_reward()[0]

                self.embed.set_field_at(index=8, name=f"Location_id_reward: {rew_loc.get_id()}", value=rew_loc.get_name())

            if not self.quest.get_explore_location() or None:
                await interaction.message.edit(embed=self.embed, view=SelectLocationView(embed=self.embed, quest=self.quest))
            else:
                await interaction.message.edit(embed=self.embed, view=None)
                await interaction.response.send_modal(AddQuestModal(modal_page=1, embed=self.embed, quest=self.quest))
                return
        await interaction.response.defer()


class AddEnemyModal(discord.ui.Modal):
    enemy_name = None
    enemy_description = None
    enemy_health = None
    enemy_runes = None

    item_drop_item_id = None
    item_drop_count = None
    item_drop_chance = None

    def __init__(self, item_drop: bool = False, enemy: Enemy() = None, embed: discord.Embed = None):
        logic = enemy.get_logic()
        super().__init__(title=f"Add Enemy with [{logic.get_name()}]-logic")
        self.item_drop = item_drop
        self.enemy = enemy
        self.embed = embed

        if item_drop:
            self.item_drop_item_id = discord.ui.TextInput(label="Item_id", style=discord.TextStyle.short,
                                                          placeholder="Enter a valid item_id..", required=True)
            self.item_drop_count = discord.ui.TextInput(label="Drop_count", style=discord.TextStyle.short,
                                                        placeholder="Enter a valid drop amount..", required=True)
            self.item_drop_chance = discord.ui.TextInput(label="Drop_chance", style=discord.TextStyle.short,
                                                         placeholder="Enter a valid drop chance in %..", required=True)

            self.add_item(self.item_drop_item_id)
            self.add_item(self.item_drop_count)
            self.add_item(self.item_drop_chance)
        else:
            self.enemy_name = discord.ui.TextInput(label="Name", style=discord.TextStyle.short,
                                                   placeholder="Enter a valid enemy name..", required=True)
            self.enemy_description = discord.ui.TextInput(label="Description", style=discord.TextStyle.long,
                                                          placeholder="Enter a valid enemy description..",
                                                          required=False)
            self.enemy_health = discord.ui.TextInput(label="Health", style=discord.TextStyle.short,
                                                     placeholder="Enter a valid health amount..", required=True)
            self.enemy_runes = discord.ui.TextInput(label="Runes", style=discord.TextStyle.short,
                                                    placeholder="Enter a valid rune amount..", required=True)

            self.add_item(self.enemy_name)
            self.add_item(self.enemy_description)
            self.add_item(self.enemy_health)
            self.add_item(self.enemy_runes)

    async def on_submit(self, interaction: discord.Interaction):
        if self.item_drop:

            item = db.get_item_from_item_id(idItem=self.item_drop_item_id)
            item.set_count(self.item_drop_count.value)
            item.set_drop_rate(self.item_drop_chance.value)

            self.enemy.set_item_rewards(item)
            if self.embed is None:
                self.embed = discord.Embed(title=f"Adding item(s) reward(s) to: [NAME: {self.enemy.get_name()} | ID: {self.enemy.get_id()}]")
                self.embed.color = discord.Color.purple()
                self.embed.set_footer(text=None)

            self.embed.add_field(name=f"Item_drop_id: {item.get_idItem()}", value=item.get_name())
            self.embed.add_field(name=f"Reward amount/count:", value=item.get_count())
            self.embed.add_field(name=f"Drop chance:", value=f"{item.get_drop_rate()}%")
            await interaction.message.edit(embed=self.embed, view=InsertEnemyHasItemView(enemy=self.enemy, mode="enemy_with_item", embed=self.embed))

        else:
            self.enemy.set_name(self.enemy_name.value)
            self.enemy.set_health(self.enemy_health.value)
            self.enemy.set_runes(self.enemy_runes.value)

            if self.enemy_description.value == "":
                self.enemy.set_description("null")
            else:
                self.enemy.set_description(self.enemy_description.value)

            preview_embed = discord.Embed(title=f"Adding {self.enemy.get_name()}")
            preview_embed.add_field(name="Enemy description:", value=self.enemy.get_description())
            preview_embed.add_field(name="Enemy health:", value=self.enemy.get_health())
            preview_embed.add_field(name="Enemy runes reward:", value=self.enemy.get_runes())
            preview_embed.add_field(name="Location:", value="Please select below..")

            await interaction.message.edit(embed=preview_embed, view=SelectLocationView(preview_embed, self.enemy))
        await interaction.response.defer()


class AddEnemyMoveModal(discord.ui.Modal):
    move_description = discord.ui.TextInput(label="Description", style=discord.TextStyle.long,
                                            placeholder="Enter a valid description..", required=True)
    move_phase = discord.ui.TextInput(label="Phase", style=discord.TextStyle.short,
                                      placeholder="Enter a valid phase number..", required=True)
    move_damage = None
    move_healing = None
    move_max_targets = None

    def __init__(self, enemy: Enemy(), move_type: str, embed: discord.Embed):
        super().__init__(title=f"Add Enemy_moves to [{enemy.get_name()}]")
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

        move = EnemyMove()
        move.set_description(self.move_description)
        move.set_type(db.get_move_type_id_from_name(self.move_type))

        self.embed.add_field(name="Move_description:", value=self.move_description)

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

        await interaction.message.edit(embed=self.embed, view=ConfirmInsertButtonView(enemy=self.enemy, mode="enemy_move", enemy_move=move))
        await interaction.response.defer()


class AddEncounterModal(discord.ui.Modal):
    def __init__(self, embed: discord.Embed = None, encounter: Encounter() = None):
        super().__init__(title="Add Encounter")
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

        await interaction.message.edit(embed=self.embed, view=ConfirmInsertButtonView(mode="encounter", encounter=self.encounter))
        await interaction.response.defer()


# Quests
class AddQuestModal(discord.ui.Modal):
    quest_title = None
    quest_description = None
    quest_cooldown = None
    quest_rune_reward = None
    quest_flask_reward = None

    quest_req_explore_count = None
    quest_req_kills = None
    quest_req_item_count = None
    quest_req_runes = None
    quest_item_id = None

    quest_item_reward_id = None
    quest_item_count = None

    def __init__(self, modal_page=None, embed: discord.Embed = None, quest: Quest() = None):
        super().__init__(title="Add Quest")
        self.modal_page = modal_page
        self.embed = embed
        self.quest = quest

        match modal_page:
            case 1:
                self.quest_title = discord.ui.TextInput(label="Title:", style=discord.TextStyle.short,
                                                        placeholder="Please enter a valid title..", required=True)
                self.quest_description = discord.ui.TextInput(label="Description:", style=discord.TextStyle.long,
                                                              placeholder="Please enter a valid description..",
                                                              required=True)
                self.quest_cooldown = discord.ui.TextInput(label="Cooldown:", style=discord.TextStyle.short,
                                                           placeholder="Please enter a valid cooldown..",
                                                           required=False)
                self.quest_rune_reward = discord.ui.TextInput(label="Rune_reward:", style=discord.TextStyle.short,
                                                              placeholder="Please enter a valid reward", required=False)
                self.quest_flask_reward = discord.ui.TextInput(label="Flask_reward:", style=discord.TextStyle.short,
                                                               placeholder="Please enter the new flask_amount", required=False)

                self.add_item(self.quest_title)
                self.add_item(self.quest_description)
                self.add_item(self.quest_cooldown)
                self.add_item(self.quest_rune_reward)
                self.add_item(self.quest_flask_reward)

            case 2:
                self.quest_req_kills = discord.ui.TextInput(label="Required Kills:", style=discord.TextStyle.short,
                                                            placeholder="Please enter a valid kill amount..",
                                                            required=False)
                self.quest_req_item_count = discord.ui.TextInput(label="Required Item Count:",
                                                                 style=discord.TextStyle.short,
                                                                 placeholder="Please enter a valid item count..",
                                                                 required=False)
                self.quest_req_runes = discord.ui.TextInput(label="Required Runes:", style=discord.TextStyle.short,
                                                            placeholder="Please enter a valid rune count..",
                                                            required=False)
                self.quest_item_id = discord.ui.TextInput(label="Item_id:", style=discord.TextStyle.short,
                                                          placeholder="Please enter a valid item_id..",
                                                          required=False)
                if self.quest.get_explore_location()[0] is not None:
                    self.quest_req_explore_count = discord.ui.TextInput(label="Required explore count:",
                                                                        style=discord.TextStyle.short,
                                                                        placeholder="Please enter a valid count..",
                                                                        required=False)
                    self.add_item(self.quest_req_explore_count)

                self.add_item(self.quest_req_kills)
                self.add_item(self.quest_req_item_count)
                self.add_item(self.quest_req_runes)
                self.add_item(self.quest_item_id)

            case 3:
                self.quest_item_reward_id = discord.ui.TextInput(label="Item_reward_id", style=discord.TextStyle.short,
                                                                 placeholder="Please enter a valid id or leave empty..",
                                                                 required=True)
                self.quest_item_count = discord.ui.TextInput(label="Item_reward_count", style=discord.TextStyle.short,
                                                             placeholder="Please enter a valid amount or leave empty..",
                                                             required=True)

                self.add_item(self.quest_item_reward_id)
                self.add_item(self.quest_item_count)

    async def on_submit(self, interaction: discord.Interaction):
        match self.modal_page:
            case 1:
                self.quest.set_title(self.quest_title)
                self.embed.set_field_at(index=0, name="Title:", value=self.quest_title)

                self.quest.set_description(self.quest_description)
                self.embed.set_field_at(index=1, name="Description:", value=self.quest_description)

                if self.quest_cooldown.value == "":
                    self.quest.set_cooldown("0")
                    self.embed.set_field_at(index=11, name="Cooldown:", value="None")
                else:
                    self.quest.set_cooldown(self.quest_cooldown.value)
                    self.embed.set_field_at(index=11, name="Cooldown:", value=self.quest.get_cooldown())

                if self.quest_rune_reward.value == "":
                    self.quest.set_rune_reward("0")
                    self.embed.set_field_at(index=7, name="Rune_reward:", value="None")
                else:
                    self.quest.set_rune_reward(self.quest_rune_reward.value)
                    self.embed.set_field_at(index=7, name="Rune_reward:", value=self.quest.get_rune_reward())

                if self.quest_flask_reward.value == "":
                    self.quest.set_flask_reward("0")
                    self.embed.set_field_at(index=12, name="Flask_reward:", value="None")
                else:
                    self.quest.set_flask_reward(self.quest_flask_reward.value)
                    self.embed.set_field_at(index=12, name="Flask_reward:", value=self.quest.get_flask_reward())

            case 2:
                if self.quest_req_kills.value == "":
                    self.quest.set_req_kills("0")
                    self.embed.set_field_at(index=2, name="Req_kills:", value="None")
                else:
                    self.quest.set_req_kills(self.quest_req_kills.value)
                    self.embed.set_field_at(index=2, name="Req_kills:", value=self.quest.get_req_kills())

                if self.quest_req_item_count.value == "":
                    self.quest.set_req_item_count("0")
                    self.embed.set_field_at(index=3, name="Req_item_count:", value="None")
                else:
                    self.quest.set_req_item_count(self.quest_req_item_count.value)
                    self.embed.set_field_at(index=3, name="Req_item_count:", value=self.quest.get_req_item_count())

                if self.quest_req_runes.value == "":
                    self.quest.set_req_runes("0")
                    self.embed.set_field_at(index=4, name="Req_runes:", value="None")
                else:
                    self.quest.set_req_runes(self.quest_req_runes.value)
                    self.embed.set_field_at(index=4, name="Req_runes:", value=self.quest.get_req_runes())

                if self.quest_item_id.value == "":
                    self.quest.set_req_item("null")
                    self.embed.set_field_at(index=5, name=f"Item_id: None", value="None")
                else:
                    self.quest.set_req_item(self.quest_item_id.value)
                    self.embed.set_field_at(index=5, name=f"Item_id: {self.quest.get_item()}",
                                            value=db.get_item_name_from_id(self.quest_item_id))

                if self.quest_req_explore_count is not None:
                    if self.quest_req_explore_count.value == "":
                        self.quest.set_req_explore_count("0")
                        self.embed.set_field_at(index=9, name="Req_explore_count:", value="None")
                    else:
                        self.quest.set_req_explore_count(self.quest_req_explore_count.value)
                        self.embed.set_field_at(index=9, name="Req_explore_count:",
                                                value=self.quest.get_req_explore_count())

                else:
                    self.quest.set_req_explore_count("0")

        match self.modal_page:
            case 1:
                await interaction.message.edit(embed=self.embed, view=NextQuestModalButtonView(modal_page=self.modal_page, quest=self.quest, embed=self.embed))
            case 2:
                if self.quest.get_req_kills() == "0":
                    self.quest.set_req_enemy(None)
                    await interaction.message.edit(embed=self.embed, view=ConfirmInsertButtonView(quest=self.quest, mode="quest"))
                else:
                    await interaction.message.edit(embed=self.embed, view=SelectEnemyLocationView(quest=self.quest, embed=self.embed, modal_page=self.modal_page))
            case 3:
                self.embed.color = discord.Color.purple()
                self.embed.title = "Adding item(s) to quest."
                self.embed.set_footer(text=None)
                self.embed.add_field(name=f"Item_Reward_id: {self.quest_item_reward_id}", value=db.get_item_name_from_id(self.quest_item_reward_id))
                self.embed.add_field(name="Reward amount/count:", value=self.quest_item_count.value)

                self.quest.set_item_reward(db.get_item_from_item_id(self.quest_item_reward_id))
                item = self.quest.get_item_reward()[0]
                item.set_count(self.quest_item_count.value)

                await interaction.message.edit(embed=self.embed, view=InsertQuestHasItemView(embed=self.embed, quest=self.quest, mode="quest_with_item"))

        await interaction.response.defer()


class SelectEnemyView(discord.ui.View):
    def __init__(self, quest: Quest()=None, embed: discord.Embed()=None, modal_page=None, location_id=None):
        super().__init__(timeout=None)
        self.add_item(SelectEnemy(quest, embed, modal_page, location_id))


class SelectEnemyLocationView(discord.ui.View):
    def __init__(self, quest: Quest() = None, embed: discord.Embed = None, modal_page: str = None):
        super().__init__(timeout=None)
        if quest:
            self.add_item(SelectEnemyLocation(quest=quest, embed=embed, modal_page=modal_page))
        else:
            self.add_item(SelectEnemyLocation())


class SelectELView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(SelectEnemyLogic())


class SelectMoveTypeView(discord.ui.View):
    def __init__(self, enemy_list: Enemy(), embed: discord.Embed):
        super().__init__(timeout=None)
        self.add_item(SelectMoveType(enemy_list, embed))


class SelectLocationView(discord.ui.View):
    def __init__(self, embed: discord.Embed = None, enemy: Enemy() = None,
                 encounter: Encounter() = None, quest: Quest() = None, index: int = None):
        super().__init__(timeout=None)

        if quest:
            if not quest.get_explore_location() and not quest.get_location_reward():
                self.add_item(SelectLocation(embed, enemy, encounter, quest, index=1))
                self.add_item(SelectLocation(embed, enemy, encounter, quest, index=2))
            elif not quest.get_explore_location():
                self.add_item(SelectLocation(embed, enemy, encounter, quest, index=1))
            elif not quest.get_location_reward():
                self.add_item(SelectLocation(embed, enemy, encounter, quest, index=2))

        else:
            self.add_item(SelectLocation(embed, enemy=enemy, encounter=encounter, quest=quest))


class InsertQuestHasItemView(discord.ui.View):
    def __init__(self, enemy: Enemy() = None, mode=None, enemy_move: EnemyMove() = None, encounter: Encounter() = None,
                 quest: Quest() = None, embed: discord.Embed = None):
        super().__init__(timeout=None)
        self.add_item(ConfirmInsertButton(enemy=enemy, mode=mode, enemy_move=enemy_move, encounter=encounter, quest=quest))
        self.add_item(InsertQuestHasItemButton(embed=embed, quest=quest))


class InsertEnemyHasItemView(discord.ui.View):
    def __init__(self, enemy: Enemy() = None, mode=None, embed: discord.Embed = None):
        super().__init__(timeout=None)
        self.add_item(ConfirmInsertButton(enemy=enemy, mode=mode))
        self.add_item(AddEnemyItemDropButton(enemy=enemy, embed=embed))


class ConfirmInsertButtonView(discord.ui.View):
    def __init__(self, enemy: Enemy() = None, mode=None, enemy_move: EnemyMove() = None, encounter: Encounter() = None, quest: Quest() = None):
        super().__init__(timeout=None)
        self.add_item(ConfirmInsertButton(enemy, mode, enemy_move, encounter, quest))


class NextQuestModalButtonView(discord.ui.View):
    def __init__(self, modal_page=None, embed: discord.Embed = None, quest: Quest() = None):
        super().__init__(timeout=None)
        self.add_item(
            NextQuestModalButton(embed=embed, modal_page=modal_page + 1, quest=quest))


class DeveloperView(discord.ui.View):

    def __init__(self, user = None):
        super().__init__()
        self.user = user.update_user()
        self.add_item(InsertEnemyButton(user=user))
        self.add_item(InsertEnemyMoveButton(user=user))
        self.add_item(InsertEncounterButton(user=user))
        self.add_item(CompleteQuestButton(user=user))
        self.add_item(InsertQuestButton(user=user))
        self.add_item(ShowSQLTXTButton(user=user))
        self.add_item(UpdateDEVMaxLocation(user=user))


class Developer(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="developer", description="Developer only.. sorry")
    async def developer(self, interaction: discord.Interaction):
        await interaction.response.defer()

        try:
            if db.validate_user(interaction.user.id):

                user = User(interaction.user.id)

                if interaction.user.id in config.botConfig["developer-ids"]:

                    embed = discord.Embed(title=f"Developer options",
                                          description="")
                    embed.add_field(name="Servers", value=f"{len(self.client.guilds)}")
                    embed.add_field(name="Users", value=f"{db.get_all_user_count()}")
                    embed.add_field(name="AVG Quest", value=f"{db.get_avg_user_quest()}")

                    await interaction.followup.send(embed=embed, view=DeveloperView(user=user))
                else:
                    await interaction.followup.send("You're not a developer!", ephemeral=True)
            else:
                await class_selection(interaction=interaction)
        except Exception as e:
            await self.client.send_error_message(e)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Developer(client))
