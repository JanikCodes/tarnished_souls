import discord
from discord.ext import commands
import db
class stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is Online. Beep bop.")

    @commands.command()
    async def stats(self, ctx):
        print("User asked for stats")
        db.validate_user(ctx.author.id, ctx.author.name)

async def setup(bot):
    await bot.add_cog(stats(bot))