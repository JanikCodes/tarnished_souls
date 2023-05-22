import random
from io import BytesIO

import discord
from discord import app_commands
from discord.ext import commands
import matplotlib.pyplot as plt
from matplotlib import ticker

import config
import db
from Classes.user import User
from Utils.classes import class_selection


class ActivityCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="activity", description="Developer only.. sorry")
    async def activity(self, interaction: discord.Interaction):
        if not interaction or interaction.is_expired():
            return

        await interaction.response.defer()

        try:
            if db.validate_user(interaction.user.id):

                if interaction.user.id in config.botConfig["developer-ids"]:

                    embed = discord.Embed(title="User Activity by Hour")

                    activity_text = str()

                    fig, ax = plt.subplots()
                    ax.bar(self.client.activity_list.keys(), self.client.activity_list.values(), color='red')
                    ax.set_xlabel('Hour')
                    ax.set_ylabel('Command Count')
                    ax.set_title('Activity by Hour')
                    ax.set_xticks(range(0, 24, 2))  # show every second hour
                    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))  # set y-axis ticks to integers

                    # Save plot to bytes buffer
                    buffer = BytesIO()
                    fig.savefig(buffer, format='png')
                    buffer.seek(0)

                    # Create Discord file object and embed
                    file = discord.File(buffer, filename='plot.png')
                    embed.set_image(url=f'attachment://plot.png')

                    embed.description = activity_text
                    await interaction.followup.send(embed=embed, file=file)
                else:
                    await interaction.followup.send("You're not a developer!", ephemeral=True)
            else:
                await class_selection(interaction=interaction)
        except Exception as e:
            await self.client.send_error_message(e)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(ActivityCommand(client))
