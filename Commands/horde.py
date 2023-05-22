import discord
from discord import app_commands
from discord.ext import commands
import db
from Classes.user import User
from Commands.fight import FightLobbyView
from Utils.classes import class_selection

MAX_USERS = 4

class HordeCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="horde", description="Fight as long as you can!")
    @app_commands.checks.has_permissions(manage_messages=True, embed_links=True, add_reactions=True,
                                         external_emojis=True, read_message_history=True, read_messages=True,
                                         send_messages=True, use_application_commands=True, use_external_emojis=True)
    async def horde(self, interaction: discord.Interaction):
        if not interaction or interaction.is_expired():
            return

        try:
            await interaction.response.defer()

            self.client.add_to_activity()

            if db.validate_user(interaction.user.id):

                user = User(interaction.user.id)
                users = [user]

                embed = discord.Embed(title=f"Public Lobby",
                                      description="",
                                      colour=discord.Color.orange())

                worldrecord_wave = db.get_highest_max_horde_wave()

                # If not solo lobby
                all_user_text = str()

                for user in users:
                    all_user_text += f"• {user.get_userName()}\n"

                embed.add_field(name=f"Horde Mode 💀", value="Defeat as many enemies as you can without dying!\n"
                                                            f"**WORLD RECORD:** `wave {worldrecord_wave}`")
                embed.add_field(name=f"Players: **{len(users)}/{MAX_USERS}**", value=all_user_text, inline=False)
                embed.set_footer(text="Enemy health is increased based on player count")

                enemy_list = db.get_all_enemies()

                await interaction.followup.send(embed=embed, view=FightLobbyView(users=users, visibility="public", enemy_list=enemy_list))
            else:
                await class_selection(interaction=interaction)
        except Exception as e:
            await self.client.send_error_message(e)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(HordeCommand(client))
