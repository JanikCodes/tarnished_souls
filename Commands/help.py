import os

import discord
from discord import app_commands
from discord.ext import commands

import db
from Classes.user import User
from Utils.classes import class_selection


class Help(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="help", description="Learn more about certain aspects of the bot")
    @app_commands.choices(choices=[
        app_commands.Choice(name="Stats", value="stats"),
        app_commands.Choice(name="Commands", value="cmds"),
        app_commands.Choice(name="Quests", value="quests"),
        app_commands.Choice(name="Items", value="items"),
    ])
    async def help(self, interaction: discord.Interaction, choices: app_commands.Choice[str]):
        selected_choice = choices.value

        match selected_choice:
            case 'stats':
                embed = discord.Embed(title=f"Information about `Character Statistics`",
                                      description=f"Depending on your selected class you'll start with different starting stats.\n"
                                                  f"**Increasing** any stat will provide **bonus effects** depending on the stat. `/upgrade strength`")
                embed.add_field(name="`Vitality`", value="**Increases** your **max health** in combat", inline=False)
                embed.add_field(name="`Mind`", value="**Increases** the amount a **flask heals** you in combat", inline=False)
                embed.add_field(name="`Endurance`", value="Grants your extra **stamina** and **reduces weight**", inline=False)
                embed.add_field(name="`Strength`, `Dexterity`, `Intelligence`, `Faith`, `Arcane`", value="**Provides bonus damage** if your weapon has the correct *scaling*", inline=False)
                embed.add_field(name="`Weight`", value="Weapons and armor have weight. The more weight you have, the less max stamina you get which is crucial for dodging.", inline=False)
                embed.colour = discord.Color.light_embed()
                await interaction.response.send_message(embed=embed)
            case 'cmds':
                all_cmds = str()
                for fileName in os.listdir('./Commands'):
                    if fileName.endswith('.py'):
                        all_cmds += f"`{fileName[:-3]}` "

                embed = discord.Embed(title=f"Information about `Commands`",
                                      description=all_cmds)
                embed.colour = discord.Color.light_embed()
                await interaction.response.send_message(embed=embed)
            case 'quests':
                embed = discord.Embed(title=f"Information about `Quests`",
                                      description=f"In order to progress through the game you'll need to complete the **main quest**. `/quest`\n"
                                                  f"*It's important to know* that if you're fighting in a group, only the host will receive the quest progress.")
                embed.add_field(name="What can I expect?",
                                value="You'll unlock more **locations**, **enemies to fight**, **items** and new **bosses**.", inline=False)
                embed.add_field(name="What if I complete all quests?",
                                value="Just like in the original game, you'll enter NG+",
                                inline=False)
                embed.add_field(name="Why is there a timer for my quest?",
                                value="This is a prevention to rush trough the quests quickly, but it only appears after major quests",
                                inline=False)

                embed.colour = discord.Color.light_embed()
                await interaction.response.send_message(embed=embed)
            case 'items':
                embed = discord.Embed(title=f"Information about `Items`",
                                      description=f"You can get new items by doing `/explore`\n"
                                                  f"While exploring your character will encounter unique and random events that can result in item drops.")
                embed.add_field(name="Item requirements", value="Most weapons have certain requirements that need to be met in order to equip that weapon. You can increase certain stats by typing `/upgrade`", inline=False)
                embed.colour = discord.Color.light_embed()
                await interaction.response.send_message(embed=embed)
async def setup(client: commands.Bot) -> None:
    await client.add_cog(Help(client), guild=discord.Object(id=763425801391308901))
