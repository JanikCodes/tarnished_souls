from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands
import db
from Classes.user import User
from Utils import utils

class Explore(commands.Cog):

    EXPLORE_TIME = 60 * 20

    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="explore", description="Explore the world, encounter events & receive items and souls!")
    async def explore(self, interaction: discord.Interaction):
        db.validate_user(interaction.user.id, interaction.user.name)
        user = User(interaction.user.id)

        date = datetime.utcnow() - datetime(1970, 1, 1)
        seconds = (date.total_seconds())

        current_time = round(seconds * 1000)
        last_time = user.get_last_explore()


        if current_time - last_time > self.EXPLORE_TIME:
            print("Finished!")
            #display a recap off the old explore message because it's finished
            await self.explore_status(interaction, percentage=100, user=user, finished=True)
        else:
            print("Updating the explore!")
            await self.explore_status(interaction, percentage=(current_time - last_time) / self.EXPLORE_TIME * 100, user=user, finished=False)

    async def explore_status(self, interaction, percentage, user, finished):
        embed = discord.Embed(title=f"**Exploring: {percentage}**")
        embed.description = "You can find items, encounter events and explore the world."
        embed.colour = discord.Color.green() if finished else discord.Color.orange()

        total_souls = 0

        seconds = self.EXPLORE_TIME * percentage / 100
        required_encounters = (seconds / self.EXPLORE_TIME * 5)

        encounters = db.get_encounters_from_user_with_id(user.get_userId())

        #TODO: Change the user_encounter table to not have a foreign key from his inventory, cuz if the player deletes the inventory item and checks /explore, the reference is missing.


        await interaction.response.send_message(embed=embed)

async def setup(client:commands.Bot) -> None:
    await client.add_cog(Explore(client), guild=discord.Object(id=763425801391308901))
