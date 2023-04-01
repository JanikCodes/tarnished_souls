import discord
from discord import app_commands
from discord.ext import commands
import db
from Classes.user import User
from Utils import utils

class Stats(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="stats", description="Display your universal character stats")
    async def stats(self, interaction: discord.Interaction):
        db.validate_user(interaction.user.id, interaction.user.name)
        user = User(interaction.user.id)

        embed = discord.Embed(title="Stats",
                              description="Below are your statistics. These statistics are universal and apply on every server with this bot.")
        embed.set_author(name=user.get_userName())
        embed.add_field(name="**Vigor: **" + str(user.get_vigor()), value=utils.create_bars(user.get_vigor(), 100) + utils.create_invisible_spaces(3) + str(user.get_vigor()) + "/100", inline=False)
        embed.add_field(name="**Mind: **" + str(user.get_mind()), value=utils.create_bars(user.get_mind(), 100) + utils.create_invisible_spaces(3) + str(user.get_mind()) + "/100", inline=False)
        embed.add_field(name="**Endurance: **" + str(user.get_endurance()), value=utils.create_bars(user.get_endurance(), 100) + utils.create_invisible_spaces(3) + str(user.get_endurance()) + "/100", inline=False)
        embed.add_field(name="**Strength: **" + str(user.get_strength()), value=utils.create_bars(user.get_strength(), 100) + utils.create_invisible_spaces(3) + str(user.get_strength()) + "/100", inline=False)
        embed.add_field(name="**Dexterity: **" + str(user.get_dexterity()), value=utils.create_bars(user.get_dexterity(), 100) + utils.create_invisible_spaces(3) + str(user.get_dexterity()) + "/100", inline=False)
        embed.add_field(name="**Intelligence: **" + str(user.get_intelligence()), value=utils.create_bars(user.get_intelligence(), 100) + utils.create_invisible_spaces(3) + str(user.get_intelligence()) + "/100", inline=False)
        embed.add_field(name="**Faith: **" + str(user.get_faith()), value=utils.create_bars(user.get_faith(), 100) + utils.create_invisible_spaces(3) + str(user.get_faith()) + "/100", inline=False)
        embed.add_field(name="**Arcane: **" + str(user.get_arcane()), value=utils.create_bars(user.get_arcane(), 100) + utils.create_invisible_spaces(3) + str(user.get_arcane()) + "/100", inline=False)

        await interaction.response.send_message(embed=embed)

async def setup(client:commands.Bot) -> None:
    await client.add_cog(Stats(client), guild=discord.Object(id=763425801391308901))
