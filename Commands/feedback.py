import discord
from discord import app_commands, ui
from discord.ext import commands

import config


class FeedbackModal(discord.ui.Modal, title="Feedback"):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    feedback = ui.TextInput(label='Feedback', style=discord.TextStyle.paragraph)
    like = ui.TextInput(label="What do you like the most? 💕", style=discord.TextStyle.paragraph)
    dislike = ui.TextInput(label="What do you dislike the most? 👎", style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            self.bot.add_to_activity()

            # get feedback results
            feedback = self.feedback.value
            like = self.like.value
            dislike = self.dislike.value

            embed = discord.Embed(title=f"New Feedback from {interaction.user.name}!",
                                  description="",
                                  colour=discord.Color.green())
            embed.add_field(name="Feedback", value=feedback, inline=False)
            embed.add_field(name="What do you like the most? 💕", value=like, inline=False)
            embed.add_field(name="What do you dislike the most? 👎", value=dislike, inline=False)

            channel = self.bot.get_guild(config.botConfig["hub-server-guild-id"]).get_channel(1097240168467017829)
            await channel.send(embed=embed)

            # show result to user for feedback
            await interaction.response.send_message(f'Thanks for your feedback, {interaction.user.name}!',
                                                    ephemeral=True, delete_after=4)
        except Exception as e:
            await self.bot.send_error_message(e)
class Feedback(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="feedback", description="In case you want to leave any feedback, ranging from balancing to simple opinion")
    async def feedback(self, interaction: discord.Interaction):
        if not interaction or interaction.is_expired():
            return

        modal = FeedbackModal(bot=self.client)
        await interaction.response.send_modal(modal)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Feedback(client))
