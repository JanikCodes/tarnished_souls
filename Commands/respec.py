import discord
from discord import app_commands
from discord.ext import commands

import db
from Classes.user import User
from Utils.classes import class_selection


class RespecCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="respec", description="Change again how you distribute your levels")
    async def respec(self, interaction: discord.Interaction, vigor: int, mind: int, endurance: int, strength: int, dexterity: int, intelligence: int, faith: int, arcane: int):
        if not interaction or interaction.is_expired():
            return

        try:
            await interaction.response.defer()

            self.client.add_to_activity()

            if db.validate_user(interaction.user.id):

                user = User(interaction.user.id)
                old_stats_text = str()
                new_stats_text = str()
                total_points = user.get_vigor() + user.get_mind() + user.get_endurance() + user.get_strength() + user.get_dexterity() + user.get_intelligence() + user.get_faith() + user.get_arcane()
                total_points_spend = vigor + mind + endurance + strength + dexterity + intelligence + faith + arcane

                # all needs to be spend
                # no attribute is allowed to be below 10
                if(vigor < 10 or mind < 10 or endurance < 10 or strength < 10 or dexterity < 10 or intelligence < 10 or faith < 10 or arcane < 10):
                    embed = discord.Embed(title=f"Failed",
                                          description="One of your attribute was below **10**. Every attribute needs to be atleast level 10!")
                    embed.colour = discord.Color.red()
                    await interaction.followup.send(embed=embed)
                    return

                if total_points > total_points_spend:
                    embed = discord.Embed(title=f"Failed",
                                          description=f"You have a total of {total_points} points to spend **but** you only spend {total_points_spend} points! \nPlease add **__{total_points - total_points_spend}__** points to any attribute.")
                    embed.colour = discord.Color.red()
                    await interaction.followup.send(embed=embed)
                    return

                if total_points < total_points_spend:
                    embed = discord.Embed(title=f"Failed",
                                          description=f"You have a total of {total_points} points to spend **but** you tried to spend {total_points_spend} points! \nPlease remove **__{total_points_spend - total_points}__**")
                    embed.colour = discord.Color.red()
                    await interaction.followup.send(embed=embed)
                    return

                old_stats_text += f"**Vig**: `{user.get_vigor()}` "
                old_stats_text += f"**Min**: `{user.get_mind()}` "
                old_stats_text += f"**End**: `{user.get_endurance()}` "
                old_stats_text += f"**Str**: `{user.get_strength()}` "
                old_stats_text += f"**Dex**: `{user.get_dexterity()}` "
                old_stats_text += f"**Int**: `{user.get_intelligence()}` "
                old_stats_text += f"**Fai**: `{user.get_faith()}` "
                old_stats_text += f"**Arc**: `{user.get_arcane()}` "

                new_stats_text += f"**Vig**: `{vigor}` "
                new_stats_text += f"**Min**: `{mind}` "
                new_stats_text += f"**End**: `{endurance}` "
                new_stats_text += f"**Str**: `{strength}` "
                new_stats_text += f"**Dex**: `{dexterity}` "
                new_stats_text += f"**Int**: `{intelligence}` "
                new_stats_text += f"**Fai**: `{faith}` "
                new_stats_text += f"**Arc**: `{arcane}` "

                embed = discord.Embed(title=f"Success", description="You've successfully changed your level distribution.")
                embed.add_field(name="Before:", value=old_stats_text, inline=False)
                embed.add_field(name="After:", value=new_stats_text, inline=False)

                embed.colour = discord.Color.green()
                db.set_stat_from_user_with_id(user.get_userId(), "vigor", vigor)
                db.set_stat_from_user_with_id(user.get_userId(), "mind", mind)
                db.set_stat_from_user_with_id(user.get_userId(), "endurance", endurance)
                db.set_stat_from_user_with_id(user.get_userId(), "strength", strength)
                db.set_stat_from_user_with_id(user.get_userId(), "dexterity", dexterity)
                db.set_stat_from_user_with_id(user.get_userId(), "intelligence", intelligence)
                db.set_stat_from_user_with_id(user.get_userId(), "faith", faith)
                db.set_stat_from_user_with_id(user.get_userId(), "arcane", arcane)

                await interaction.followup.send(embed=embed)
            else:
                await class_selection(interaction=interaction)
        except Exception as e:
            await self.client.send_error_message(e)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(RespecCommand(client))
