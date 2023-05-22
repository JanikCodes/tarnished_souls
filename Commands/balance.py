import random

import discord
from discord import app_commands
from discord.ext import commands

import config
import db
from Classes.user import User
from Utils.classes import class_selection


class BalanceCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="balance", description="Developer only.. sorry")
    async def balance(self, interaction: discord.Interaction, id_location: int, avg_min_damage: int, avg_max_damage: int, boss_extra_dmg: int):
        if not interaction or interaction.is_expired():
            return

        try:
            await interaction.response.defer()

            if db.validate_user(interaction.user.id):

                if interaction.user.id in config.botConfig["developer-ids"]:

                    enemy_list = db.get_enemies_from_location(location_id=id_location)

                    for enemy in enemy_list:
                        total_moves = len(enemy.moves)
                        enemy_average_damage_per_turn = random.randint(avg_min_damage, avg_max_damage)

                        if enemy.description.upper() == "BOSS":
                            print("Adjusted boss dmg..")
                            enemy_average_damage_per_turn += boss_extra_dmg

                        enemy_attack_move_count = sum(move.get_type() == 1 for move in enemy.moves)
                        for move in enemy.moves:
                            if move.get_type() == 1:
                                move_damage = self.calculate_move_damage(enemy_average_damage_per_turn,
                                                                    enemy_attack_move_count, total_moves)
                                move_damage += random.randint(-4, 4)
                                db.update_enemy_move_damage(move.get_id(), move_damage)

                    await interaction.followup.send(f"Auto balanced all enemies with `AVG {avg_min_damage} - {avg_max_damage}` (Boss: +{boss_extra_dmg}) damage at location `ID {id_location}`")
                else:
                    await interaction.followup.send("You're not a developer!", ephemeral=True)
            else:
                await class_selection(interaction=interaction)
        except Exception as e:
            await self.client.send_error_message(e)

    def calculate_move_damage(self, enemy_average_damage_per_turn, enemy_attack_move_count, total_moves):
        move_selection_chance = 1 / total_moves
        move_damage = enemy_average_damage_per_turn / (enemy_attack_move_count * move_selection_chance)
        return move_damage

async def setup(client: commands.Bot) -> None:
    await client.add_cog(BalanceCommand(client))
