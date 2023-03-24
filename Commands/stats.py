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
    async def stats(self, ctx):
        print("Stats was called!")
        if database.does_user_exist(ctx.author.id):
            await ctx.send("You exist!")
        else:
            await ctx.send("You don't exist yet.. I'll create you in the database.")
            database.add_user(ctx.author.id, ctx.author.name)

async def setup(bot):
    await bot.add_cog(stats(bot))