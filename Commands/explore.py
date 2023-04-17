import math
import random
import time

import discord
from discord import app_commands
from discord.ext import commands

import db
from Classes.user import User
from Utils.classes import class_selection

EXPLORE_TIME = 60 * 10
ENCOUNTER_AMOUNT = 5
BASE_RUNE_REWARD = 200

class Explore(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="explore", description="Explore the world, encounter events & receive items and souls!")
    async def explore(self, interaction: discord.Interaction):
        try:
            if db.validate_user(interaction.user.id):
                user = User(interaction.user.id)

                current_time = (round(time.time() * 1000)) // 1000
                last_time = user.get_last_explore()

                if float(current_time) - float(last_time) > EXPLORE_TIME:
                    # display a recap off the old explore message because it's finished
                    await self.explore_status(interaction, percentage=100, user=user, finished=True)
                    db.remove_user_encounters(idUser=user.get_userId())
                    db.update_last_explore_timer_from_user_with_id(idUser=user.get_userId(), current_time=current_time)
                else:
                    await self.explore_status(interaction, percentage=(current_time - last_time) / EXPLORE_TIME * 100,
                                              user=user, finished=False)
            else:
                await class_selection(interaction=interaction)
        except Exception as e:
            await self.client.send_error_message(e)

    async def explore_status(self, interaction, percentage, user, finished):
        embed = discord.Embed(title=f"**Exploring: {percentage:.1f}%**")
        embed.description = "You can find items, encounter events and explore the world."
        embed.colour = discord.Color.green() if finished else discord.Color.orange()

        total_runes = 0

        seconds = EXPLORE_TIME * percentage / 100
        required_encounters = int((seconds / EXPLORE_TIME * ENCOUNTER_AMOUNT))

        encounters = db.get_encounters_from_user(user=user)
        # display previous encounters
        for i in range(0, len(encounters)):
            loot_sentence = str()

            item = db.get_item_from_user_encounter_with_enc_id(idUser=user.get_userId(),
                                                               idEncounter=encounters[i].get_id())

            if item:
                # received a drop
                emoji = discord.utils.get(self.client.get_guild(763425801391308901).emojis,
                                          name=item.get_iconCategory())
                loot_sentence = f"\n **:grey_exclamation:Found:** {emoji} `{item.get_name()}` {item.get_extra_value_text()}"

            embed.add_field(
                name=f"*After {math.ceil(EXPLORE_TIME / 60 / ENCOUNTER_AMOUNT * i + 1)} minutes..*",
                value=encounters[i].get_description() + loot_sentence, inline=False)

        # generate new encounters
        for i in range(0, required_encounters - (len(encounters))):
            new_encounter = db.create_new_encounter_from_location(user.get_userId(), user.get_current_location().get_id())
            loot_sentence = str()

            if new_encounter:
                if new_encounter.get_drop_rate() >= random.randint(0, 100):
                    # we received an item drop!
                    all_item_ids = db.get_all_item_ids()
                    random_item_id = random.choice(all_item_ids)
                    item = db.get_item_from_item_id(random_item_id)
                    random_stats = self.calculate_random_stats()
                    item.set_extra_value(random_stats)

                    emoji = discord.utils.get(self.client.get_guild(763425801391308901).emojis,
                                              name=item.get_iconCategory())

                    db.add_item_to_user(idUser=user.get_userId(), item=item)
                    db.update_user_encounter_item(idEncounter=new_encounter.get_id(), item=item, idUser=user.get_userId())

                    loot_sentence = f"\n **:grey_exclamation:Found:** {emoji} `{item.get_name()}` {item.get_extra_value_text()}"
                else:
                    pass

                embed.add_field(
                    name=f"*After {math.ceil(EXPLORE_TIME / 60 / ENCOUNTER_AMOUNT * (len(encounters) + i + 1))} minutes..*",
                    value=new_encounter.get_description() + loot_sentence, inline=False)
            else:
                print(f"WARNING: Not enough encounters for location: {user.get_current_location().get_name()}")
        if not finished:
            embed.add_field(name=". . .", value="", inline=False)
        else:
            # grant runes as reward
            rune_amount = int(( ENCOUNTER_AMOUNT * BASE_RUNE_REWARD + user.get_all_stat_levels() ) * user.get_all_stat_levels() / 15)
            db.increase_runes_from_user_with_id(idUser=user.get_userId(), amount=rune_amount)

            # update quest progress for host
            db.check_for_quest_update(idUser=user.get_userId(), runes=rune_amount, explore_location_id=user.get_current_location().get_id())

            embed.set_footer(text=f"You've received {rune_amount} runes!")

        await interaction.response.send_message(embed=embed)

    def calculate_random_stats(self):
        # 25% chance of triggering random stats
        if 25 >= random.randint(0, 100):
            mean = 3  # The center of the range (0-10)
            std_deviation = 2  # Controls how spread out the distribution is

            # Generate a random number using a Gaussian distribution
            number = random.gauss(mean, std_deviation)

            # Keep the number within the range of 0-10
            number = max(0, min(10, number))

            return math.ceil(number)
        else:
            return 0


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Explore(client))
