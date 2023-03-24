import discord
from discord.ext import commands
import database

class stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is Online. Beep bop.")

    @commands.command()
    async def stats(selfself, ctx):
        await ctx.send("Hey!")

async def setup(bot):
    await bot.add_cog(stats(bot))