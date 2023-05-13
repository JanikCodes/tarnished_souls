import random

import discord
from discord import app_commands
from discord.ext import commands

import db
from Classes.enemy import Enemy
from Classes.user import User
from Commands.fight import Fight
from Utils.classes import class_selection


class InvadeCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="invade", description="Invade your current location to fight another player!")
    async def invade(self, interaction: discord.Interaction):

        try:
            if db.validate_user(interaction.user.id):
                user = User(interaction.user.id)

                enemy_user = User(random.choice(db.get_all_user_ids_from_location(location=user.get_current_location(), himself=user.get_userId())))

                # TODO: Get enemy template from user weapon iconCategory
                enemy_template = Enemy(idEnemy=26)
                enemy_template.is_player = enemy_user
                enemy_template.overwrite_moves_with_damage()
                enemy_template.overwrite_alL_move_descriptions(enemy_user.get_userName())
                enemy_template.set_max_health(enemy_user.get_max_health())
                enemy_template.set_name(enemy_user.get_userName())
                enemy_template.set_runes(int(enemy_user.get_max_health() / 2))

                fight = Fight(enemy_list=[enemy_template], users=[user], interaction=interaction, turn_index=0, enemy_index=0)
                await fight.update_fight_battle_view(force_idle_move=True)

            else:
                await class_selection(interaction=interaction)
        except Exception as e:
            await self.client.send_error_message(e)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(InvadeCommand(client))
