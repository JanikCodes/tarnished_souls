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
    async def balance(self, interaction: discord.Interaction, id_location: int, avg_min_damage: int, avg_max_damage: int, min_health: int, boss_extra_dmg: int, boss_extra_health: int):
        if not interaction or interaction.is_expired():
            return

        try:
            await interaction.response.defer()

            if db.validate_user(interaction.user.id):

                if interaction.user.id in config.botConfig["developer-ids"]:

                    enemy_list = db.get_enemies_from_location(location_id=id_location)
                    count = 0
                    for enemy in enemy_list:
                        total_moves = len(enemy.moves)
                        enemy_average_damage_per_turn = random.randint(avg_min_damage, avg_max_damage)

                        raw_enemy_health = min_health + (count * 125)
                        new_enemy_health = random.randint(raw_enemy_health - 200, raw_enemy_health)
                        new_enemy_healing = int(min_health / 8)
                        new_runes = new_enemy_health / 6
                        count += 1

                        if enemy.description.upper() == "BOSS":
                            print(f"Adjusted balance for location [{id_location}]")
                            enemy_average_damage_per_turn += boss_extra_dmg
                            new_enemy_health += boss_extra_health

                        db.update_enemy_move_healing(enemy.get_id(), new_enemy_healing)
                        db.update_enemy_health(enemy.get_id(), new_enemy_health)
                        db.update_enemy_runes(enemy.get_id(), new_runes)

                        enemy_attack_move_count = sum(move.get_type() == 1 for move in enemy.moves)
                        for move in enemy.moves:
                            if move.get_type() == 1:
                                move_damage = self.calculate_move_damage(enemy_average_damage_per_turn,
                                                                    enemy_attack_move_count, total_moves)
                                move_damage += random.randint(-4, 4)
                                db.update_enemy_move_damage(move.get_id(), move_damage)


                    await interaction.followup.send(f"Auto balanced all enemies with `AVG {avg_min_damage} - {avg_max_damage}` (Boss: +{boss_extra_dmg}) damage,  `{min_health}` (Boss: +{boss_extra_health}) health at location `ID {id_location}`")
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
