import discord
from discord.ext import commands

import Utils.utils
import db
from Classes.user import User
from Utils import utils


class stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is Online. Beep bop.")

    @commands.command()
    async def stats(self, ctx):
        db.validate_user(ctx.author.id, ctx.author.name)
        user = User(ctx.author.id)
        # Create a new embed
        embed = discord.Embed(title="Stats", description='Below are your statistics. These statistics are universal and apply on every server with this bot.')
        embed.set_author(name=user.get_userName())
        embed.add_field(name="**Vigor: **" + str(user.get_vigor()), value=utils.create_bars(user.get_vigor(), 100) + utils.create_invisible_spaces(3) + str(user.get_vigor()) + "/100", inline=False)
        embed.add_field(name="**Mind: **" + str(user.get_mind()), value= utils.create_bars(user.get_mind(), 100) + utils.create_invisible_spaces(3) + str(user.get_mind()) + "/100", inline=False)
        embed.add_field(name="**Endurance: **" + str(user.get_endurance()), value= utils.create_bars(user.get_endurance(), 100) + utils.create_invisible_spaces(3) + str(user.get_endurance()) + "/100", inline=False)
        embed.add_field(name="**Strength: **" + str(user.get_strength()), value=utils.create_bars(user.get_strength(), 100) + utils.create_invisible_spaces(3) + str(user.get_strength()) + "/100", inline=False)
        embed.add_field(name="**Dexterity: **" + str(user.get_dexterity()), value= utils.create_bars(user.get_dexterity(), 100) + utils.create_invisible_spaces(3) + str(user.get_dexterity()) + "/100", inline=False)
        embed.add_field(name="**Intelligence: **" + str(user.get_intelligence()), value= utils.create_bars(user.get_intelligence(), 100) + utils.create_invisible_spaces(3) + str(user.get_intelligence()) + "/100", inline=False)
        embed.add_field(name="**Faith: **" + str(user.get_faith()), value= utils.create_bars(user.get_faith(), 100) + utils.create_invisible_spaces(3) + str(user.get_faith()) + "/100", inline=False)
        embed.add_field(name="**Arcane: **" + str(user.get_arcane()), value= utils.create_bars(user.get_arcane(), 100) + utils.create_invisible_spaces(3) + str(user.get_arcane()) + "/100", inline=False)
        # Send the embed as a response to the user
        await ctx.send(embed= embed)


async def setup(bot):
    await bot.add_cog(stats(bot))