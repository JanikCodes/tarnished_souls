import datetime

import discord
from discord import app_commands
from discord.ext import commands
import db
from Classes.user import User
from Utils.classes import class_selection
import time

class FinishQuest(discord.ui.Button):
    def __init__(self, user, current_quest):
        super().__init__(label='Complete Quest', style=discord.ButtonStyle.success)
        self.user = user
        self.current_quest = current_quest
    async def callback(self, interaction: discord.Interaction):

        if interaction.user.id != int(self.user.get_userId()):
            embed = discord.Embed(title=f"You're not allowed to use this action!",
                                  description="",
                                  colour=discord.Color.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=2)

        await interaction.response.defer()

        # Check if user even has the quest anymore
        if not db.get_user_quest_with_quest_id(idUser=self.user.get_userId(), idQuest=self.current_quest.get_quest().get_id()):
            message = interaction.message
            edited_embed = message.embeds[0]
            edited_embed.colour = discord.Color.red()
            await interaction.message.edit(embed=edited_embed, view=None)
            return

        # Give out quest rewards to user
        # Add runes
        if self.current_quest.get_quest().get_rune_reward() > 0:
            db.increase_runes_from_user_with_id(idUser=self.user.get_userId(), amount=self.current_quest.get_quest().get_rune_reward())
        # Add new Location
        if self.current_quest.get_quest().get_location_reward():
            db.update_max_location_from_user(idUser=self.user.get_userId(), idLocation=self.current_quest.get_quest().get_location_reward().get_id())
        # Add Item
        if len(self.current_quest.get_quest().get_item_reward()) > 0:
            for item in self.current_quest.get_quest().get_item_reward():
                db.add_item_to_user(idUser=self.user.get_userId(), item=item)
        # Increase flask amount
        if self.current_quest.get_quest().get_flask_reward() > 0:
            db.update_flask_amount_from_user(idUser=self.user.get_userId(), amount=self.current_quest.get_quest().get_flask_reward())

        # Edit quest message
        message = interaction.message
        edited_embed = message.embeds[0]
        edited_embed.colour = discord.Color.green()
        db.remove_quest_from_user_with_quest_id(idUser=self.user.get_userId(), idQuest=self.current_quest.get_quest().get_id())
        db.add_quest_to_user(idUser=self.user.get_userId(), idQuest=self.current_quest.get_quest().get_id() + 1)

        # update timer in case cooldown exist
        current_time = (round(time.time() * 1000)) // 1000
        db.update_last_quest_timer_from_user_with_id(idUser=self.user.get_userId(), current_time=current_time)
        await interaction.message.edit(embed=edited_embed, view=None)

class QuestView(discord.ui.View):
    def __init__(self, user, current_quest):
        super().__init__()
        self.user = user.update_user()
        self.add_item(FinishQuest(user=user, current_quest=current_quest))

class Quest(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="quest", description="Try completing the quest-line")
    async def quest(self, interaction: discord.Interaction):
        print("Quest")
        if not interaction or interaction.is_expired():
            return

        try:
            await interaction.response.defer()

            self.client.add_to_activity()

            if db.validate_user(interaction.user.id):

                user = User(interaction.user.id)

                current_quest = db.get_current_user_quest(idUser=user.get_userId())

                if current_quest is None:
                    # create new quest rel
                    current_quest = db.add_init_quest_to_user(idUser=user.get_userId())

                current_time = (round(time.time() * 1000)) // 1000
                last_time = user.get_last_quest()

                if float(current_time) - float(last_time) > current_quest.quest.get_cooldown():
                    # finished
                    embed = discord.Embed(title=f"{user.get_userName()}'s current quest:",
                                          description=f"**{current_quest.quest.get_title()}** \n{current_quest.quest.get_description()}")

                    embed.add_field(name="Progress:", value=current_quest.get_quest_progress_text(), inline=False)

                    if current_quest.has_rewards():
                        embed.add_field(name="Rewards:", value=current_quest.get_quest_reward_text(interaction=interaction), inline=False)

                    if current_quest.is_finished():
                        await interaction.followup.send(embed=embed, view=QuestView(user=user, current_quest=current_quest))
                    else:
                        await interaction.followup.send(embed=embed)
                else:
                    embed = discord.Embed(title=f"Quest on cooldown..",
                                          description=f"Your next quest will be available in: {str(datetime.timedelta(seconds=current_quest.quest.get_cooldown() - (float(current_time) - float(last_time))))}",
                                          colour=discord.Color.red())
                    await interaction.followup.send(embed=embed)
            else:
                await class_selection(interaction=interaction)
        except Exception as e:
            await self.client.send_error_message(e)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Quest(client))
