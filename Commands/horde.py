import discord
from discord import app_commands
from discord.ext import commands

import db
from Classes.user import User
from Commands.fight import JoinButton, Fight
from Utils.classes import class_selection

MAX_USERS = 4
STAMINA_REGEN = 7
STAMINA_COST = 45
HEAL_AMOUNT = 380

class StartButton(discord.ui.Button):
    def __init__(self, users, enemy_list):
        super().__init__(label='Start!', style=discord.ButtonStyle.primary)
        self.users = users
        self.enemy_list = enemy_list

    async def callback(self, interaction: discord.Interaction):
        if str(interaction.user.id) != self.users[0].get_userId():
            embed = discord.Embed(title=f"You're not allowed to start the fight.",
                                  description="",
                                  colour=discord.Color.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=2)
        await interaction.response.defer()

        fight = Fight(enemy=self.enemy_list[0], users=self.users, interaction=interaction, turn_index=0)
        await fight.update_fight_battle_view()

class FightLobbyView(discord.ui.View):
    def __init__(self, users, enemy_list, visibility):
        super().__init__()

        # disable join button if reached max users
        disable = False
        if len(users) == MAX_USERS:
            disable = True

        self.add_item(StartButton(users=users, enemy_list=enemy_list))
        if visibility == 'public':
            self.add_item(JoinButton(users=users, disabled=disable))


class HordeCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="horde", description="Fight as long as you can!")
    async def horde(self, interaction: discord.Interaction):
        await interaction.response.defer()

        try:
            if db.validate_user(interaction.user.id):

                user = User(interaction.user.id)

                embed = discord.Embed(title=f"Public Lobby",
                                      description="",
                                      colour=discord.Color.orange())

                embed.add_field(name=f"Horde Mode 💀", value="Defeat as many enemies as you can without dying!")
                embed.add_field(name=f"Players: **1/{MAX_USERS}**", value="", inline=False)
                embed.set_footer(text="Click the button below in order to join!")

                enemy_list = db.get_all_enemies()

                await interaction.followup.send(embed=embed, view=FightLobbyView(users=[user], visibility="public", enemy_list=enemy_list))
            else:
                await class_selection(interaction=interaction)
        except Exception as e:
            await self.client.send_error_message(e)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(HordeCommand(client))
