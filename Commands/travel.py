import discord
from discord import app_commands
from discord.ext import commands
import db
from Classes.user import User
from Utils.classes import class_selection


class TravelView(discord.ui.View):
    def __init__(self):
        super().__init__()

        # Set up the initial options for the select menu
        self.select = discord.ui.Select(
            placeholder="Choose a new location!",
            min_values=1,
            max_values=1,
            options=[
                discord.SelectOption(
                    label="Limgrave",
                    description="Limgrave is a lush, expansive section of the Tenebrae Demesne"
                ),
                discord.SelectOption(
                    label="Weeping Peninsula",
                    description="The peninsula, to Limgrave's south, is named for its unceasing rainfall, redolent of lament."
                ),
                discord.SelectOption(
                    label="Liurnia of the lakes",
                    description="With its forests perpetually blanketed in fog, eerie sounds of bells can be heard in the distance."
                )
            ]
        )

        # Add the select menu to the view
        self.add_item(self.select)

    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        await interaction.response.edit_message(content=f"Awesome! I like {select.values[0]} too!")

class Travel(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="travel", description="Travel to to various places in order to earn different loot or encounter new enemies.")
    async def travel(self, interaction: discord.Interaction):
        if db.validate_user(interaction.user.id):
            user = User(interaction.user.id)

            embed = discord.Embed(title=f"{user.get_userName()} is resting at a grace..",
                                  description=f"You're currently at **X**. Please choose your next destination.")

            embed.set_footer(text="You'll unlock more locations by simply playing the bot & completing quests")

            await interaction.response.send_message(embed=embed, view=TravelView())
        else:
            await class_selection(interaction=interaction)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Travel(client), guild=discord.Object(id=763425801391308901))
