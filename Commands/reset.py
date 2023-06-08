import discord
from discord import app_commands
from discord.ext import commands

import db
from Classes.user import User
from Utils.classes import class_selection


class ChoiceButton(discord.ui.Button):
    def __init__(self, label, style, user, func):
        super().__init__(label=label, style=style)
        self.user = user
        self.func = func

    async def callback(self, interaction: discord.Interaction):

        if interaction.user.id != int(self.user.get_userId()):
            embed = discord.Embed(title=f"You're not allowed to use this action!",
                                  description="",
                                  colour=discord.Color.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=2)

        await interaction.response.defer()

        if self.func == 'yes':
            message = interaction.message
            edited_embed = message.embeds[0]
            edited_embed.colour = discord.Color.green()

            db.reset_user(idUser=self.user.get_userId())

            edited_embed.add_field(name="Success", value="You've successfully reset your whole character..", inline=False)

            await interaction.message.edit(embed=edited_embed, view=None, delete_after=2)
        else:
            message = interaction.message
            edited_embed = message.embeds[0]
            edited_embed.colour = discord.Color.red()

            edited_embed.add_field(name="Aborted", value="This process has been aborted!", inline=False)

            await interaction.message.edit(embed=edited_embed, view=None, delete_after=2)


class ResetView(discord.ui.View):

    def __init__(self, user):
        super().__init__()
        self.user = user.update_user()
        self.add_item(ChoiceButton(label="Yes", style=discord.ButtonStyle.success, user=user, func='yes'))
        self.add_item(ChoiceButton(label="No", style=discord.ButtonStyle.danger, user=user, func='no'))

class Reset(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="reset", description="You can decide if you want to reset your whole character!")
    async def reset(self, interaction: discord.Interaction):
        if not interaction or interaction.is_expired():
            return

        try:
            await interaction.response.defer()

            self.client.add_to_activity()
            
            if db.validate_user(interaction.user.id):

                user = User(interaction.user.id)

                embed = discord.Embed(title=f"Account deletion",
                                      description=f"<@{user.get_userId()}> are you sure that you want to **reset** your **whole character**?")
                embed.add_field(name="What will be lost:", value="- stats\n"
                                                                 "- items\n"
                                                                 "- progress\n"
                                                                 "- **everything**", inline=False)

                await interaction.followup.send(embed=embed, view=ResetView(user=user))
            else:
                await class_selection(interaction=interaction)
        except Exception as e:
            await self.client.send_error_message(e)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Reset(client))
