import random
import time
from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands
import db
from Classes.encounter import Encounter
from Classes.user import User
from Utils import utils

class Explore(commands.Cog):

    EXPLORE_TIME = 60 * 20
    ENCOUNTER_AMOUNT = 5

    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="explore", description="Explore the world, encounter events & receive items and souls!")
    async def explore(self, interaction: discord.Interaction):
        db.validate_user(interaction.user.id, interaction.user.name)
        user = User(interaction.user.id)

        current_time = (round(time.time() * 1000)) // 1000
        last_time = user.get_last_explore()
        print(current_time - last_time)

        if float(current_time) - float(last_time) > self.EXPLORE_TIME:
            print("Finished!")
            #display a recap off the old explore message because it's finished
            await self.explore_status(interaction, percentage=100, user=user, finished=True)
            db.remove_user_encounters(idUser=user.get_userId())
            db.update_last_explore_timer_from_user_with_id(idUser=user.get_userId(), current_time=current_time)
        else:
            print("Updating the explore!")
            await self.explore_status(interaction, percentage=(current_time - last_time) / self.EXPLORE_TIME * 100, user=user, finished=False)

    async def explore_status(self, interaction, percentage, user, finished):
        embed = discord.Embed(title=f"**Exploring: {percentage}%**")
        embed.description = "You can find items, encounter events and explore the world."
        embed.colour = discord.Color.green() if finished else discord.Color.orange()

        total_souls = 0

        seconds = self.EXPLORE_TIME * percentage / 100
        required_encounters = int((seconds / self.EXPLORE_TIME * self.ENCOUNTER_AMOUNT))

        encounters = db.get_encounters_from_user_with_id(user.get_userId())
        # display previous encounters
        for i in range(0, len(encounters)):
            loot_sentence = str()

            item = db.get_item_from_user_encounter_with_rel_id(db.get_item_id_from_user_encounter(idUser=user.get_userId(), idRel=encounters[i].get_id()))

            if item:
                #received a drop
                loot_sentence = f"\n **:grey_exclamation:Recieved:** `{item.get_name()}` {item.get_extra_value_text()}"

            embed.add_field(name=f"*After {(i + 1) * (int) (self.EXPLORE_TIME / self.ENCOUNTER_AMOUNT / 60)} minutes..*", value=encounters[i].get_description() + loot_sentence, inline=False)

        # generate new encounters
        for i in range(0, required_encounters - (len(encounters))):
            new_encounter = db.create_new_encounter(user.get_userId())

            if new_encounter.get_drop_rate() >= random.randint(0, 100):
                # we recieved an item drop!
                pass

            embed.add_field(name=f"*After { ((len(encounters) + (i + 1)) * self.EXPLORE_TIME / self.ENCOUNTER_AMOUNT / 60) } minutes..*", value=new_encounter.get_description(), inline=False)

        if not finished:
            embed.add_field(name=". . .", value="", inline=False)


        await interaction.response.send_message(embed=embed)

async def setup(client:commands.Bot) -> None:
    await client.add_cog(Explore(client), guild=discord.Object(id=763425801391308901))
