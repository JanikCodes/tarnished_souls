import discord
from discord import app_commands
from discord.ext import commands
import db
from Classes.user import User
from Utils.classes import class_selection

class TravelSelect(discord.ui.Select):
    def __init__(self, user):
        super().__init__(placeholder="Choose a location..")
        self.user = user

        for location in db.get_all_locations_from_user(user=user):
            self.add_option(label=f"{location.get_name()}", value=f"{location.get_id()}")

    async def callback(self, interaction: discord.Interaction):

        await interaction.response.defer()

        target_location = db.get_location_from_id(self.values[0])

        if target_location.get_id() != self.user.get_current_location().get_id():
            # new location
            message = interaction.message
            edited_embed = message.embeds[0]
            edited_embed.description = f"You've successfully traveled towards **{target_location.get_name()}**!"
            edited_embed.colour = discord.Color.green()

            db.update_location_from_user(idUser=self.user.get_userId(), idLocation=target_location.get_id())

            await interaction.message.edit(embed=edited_embed, view=None)
        else:
            # same location
            message = interaction.message
            edited_embed = message.embeds[0]
            edited_embed.description = f"You're already in **{target_location.get_name()}**.\n Please choose a different location.."
            edited_embed.colour = discord.Color.yellow()

            await interaction.message.edit(embed=edited_embed, view=TravelView(user=self.user))

class TravelView(discord.ui.View):
    def __init__(self, user):
        super().__init__()

        # Add the select menu to the view
        self.add_item(TravelSelect(user=user))

class Travel(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="travel", description="Travel to to various places in order to earn different loot or encounter new enemies.")
    async def travel(self, interaction: discord.Interaction):
        if db.validate_user(interaction.user.id):
            user = User(interaction.user.id)

            embed = discord.Embed(title=f"{user.get_userName()} is resting at a grace..",
                                  description=f"You're currently at **{user.get_current_location().get_name()}**. Please choose your next destination.")

            embed.set_footer(text="You'll unlock more locations by simply playing the bot & completing quests")

            await interaction.response.send_message(embed=embed, view=TravelView(user=user))
        else:
            await class_selection(interaction=interaction)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Travel(client), guild=discord.Object(id=763425801391308901))
