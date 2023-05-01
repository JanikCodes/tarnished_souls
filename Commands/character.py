import discord
from discord import app_commands
from discord.ext import commands

import config
import db
from Classes.user import User
from Utils import utils
from Utils.classes import class_selection


class Character(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.rename(optional_user='user')
    @app_commands.command(name="character", description="Display your character stats & equipment")
    async def character(self, interaction: discord.Interaction, optional_user: discord.Member = None):
        await interaction.response.defer()

        try:
            if db.validate_user(interaction.user.id):

                if optional_user:
                    # check if user exists in db
                    if db.validate_user(userId=optional_user.id):
                        user = User(optional_user.id)
                    else:
                        embed = discord.Embed(title=f"User doesn't exist yet..",
                                              description="The user needs to choose a class first by typing any command like `/explore` or `/quest`",
                                              colour=discord.Color.red())
                        return await interaction.followup.send(embed=embed)
                else:
                    user = User(interaction.user.id)

                embed = discord.Embed(title=f"Character Information",
                                      description=f"Below is <@{user.get_userId()}> character information.\nThis character is universal and the same on every server *unless you do* `/reset`")

                stats_text = str()
                stats_text += f"**Level**: `{user.get_level()}` \n"
                stats_text += f"**Vig**: `{user.get_vigor()}` "
                stats_text += f"**Min**: `{user.get_mind()}` "
                stats_text += f"**End**: `{user.get_endurance()}` "
                stats_text += f"**Str**: `{user.get_strength()}` "
                stats_text += f"**Dex**: `{user.get_dexterity()}` "
                stats_text += f"**Int**: `{user.get_intelligence()}` "
                stats_text += f"**Fai**: `{user.get_faith()}` "
                stats_text += f"**Arc**: `{user.get_arcane()}` "

                embed.add_field(name="Statistics:", value=stats_text, inline=False)

                embed.add_field(name="", value=f"**Total Damage:** `{str(0) if not user.get_weapon() else user.get_weapon().get_total_value(user)}`", inline=True)
                embed.add_field(name="",value=f"**Total Armor:** `{user.get_total_armor()}`", inline=True)
                embed.add_field(name="",value=f"**Total Weight:** `{user.get_total_weight()}`", inline=True)
                embed.add_field(name="", value=f"**Max Health:** `{user.get_max_health()}`", inline=True)
                embed.add_field(name="", value=f"**Max Stamina:** `{user.get_max_stamina()}`", inline=True)
                embed.add_field(name="", value=f"**Max Flasks:** `{user.get_remaining_flasks()}`", inline=True)

                eq_text = str()
                eq_text += f"**Weapon:**\n"

                if user.get_weapon():
                    category_emoji = discord.utils.get(interaction.client.get_guild(config.botConfig["hub-server-guild-id"]).emojis, name=user.get_weapon().get_iconCategory())
                    eq_text += f"{category_emoji} `{user.get_weapon().get_name()}` **Damage:** `{user.get_weapon().get_total_value(user)}` **Weight:** `{user.get_weapon().get_weight()}` \n"

                eq_text += f"**Armor:**\n"

                if user.get_head():
                    category_emoji = discord.utils.get(interaction.client.get_guild(config.botConfig["hub-server-guild-id"]).emojis, name=user.get_head().get_iconCategory())
                    eq_text += f"{category_emoji} `{user.get_head().get_name()}` **Armor:** `{user.get_head().get_total_value(user)}` **Weight:** `{user.get_head().get_weight()}` \n"
                if user.get_chest():
                    category_emoji = discord.utils.get(interaction.client.get_guild(config.botConfig["hub-server-guild-id"]).emojis,name=user.get_chest().get_iconCategory())
                    eq_text += f"{category_emoji} `{user.get_chest().get_name()}` **Armor:** `{user.get_chest().get_total_value(user)}` **Weight:** `{user.get_chest().get_weight()}` \n"
                if user.get_legs():
                    category_emoji = discord.utils.get(interaction.client.get_guild(config.botConfig["hub-server-guild-id"]).emojis,name=user.get_legs().get_iconCategory())
                    eq_text += f"{category_emoji} `{user.get_legs().get_name()}` **Armor:** `{user.get_legs().get_total_value(user)}` **Weight:** `{user.get_legs().get_weight()}` \n"
                if user.get_gauntlet():
                    category_emoji = discord.utils.get(interaction.client.get_guild(config.botConfig["hub-server-guild-id"]).emojis,name=user.get_gauntlet().get_iconCategory())
                    eq_text += f"{category_emoji} `{user.get_gauntlet().get_name()}` **Armor:** `{user.get_gauntlet().get_total_value(user)}` **Weight:** `{user.get_gauntlet().get_weight()}`"

                embed.add_field(name="Equipment:", value=eq_text, inline=False)

                await interaction.followup.send(embed=embed)
            else:
                await class_selection(interaction=interaction)
        except Exception as e:
            await self.client.send_error_message(e)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Character(client))
