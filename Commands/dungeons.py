import discord
from discord import app_commands
from discord.ext import commands

import db
from Classes.user import User
from Classes.dungeon import Dungeon
from Utils.classes import class_selection

import json


class Dungeons(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="dungeons", description="Explore available dungeons and earn items!")
    async def dungeons(self, interaction: discord.Interaction, dungeon_name: str):
        if not interaction or interaction.is_expired():
            return

        try:
            await interaction.response.defer()

            self.client.add_to_activity()

            if db.validate_user(interaction.user.id):
                user = User(interaction.user.id)

                with open('Utils/dungeon_locations.json', 'r') as locations_file:
                    dungeon_locations = json.load(locations_file)

                target_dungeon = dungeon_name

                if target_dungeon in dungeon_locations:
                    dungeons = dungeon_locations[target_dungeon]

                    for the_dungeon in dungeons:
                        dungeon = Dungeon()
                        dungeon.set_id(1)
                        dungeon.set_title(the_dungeon['name'])
                        dungeon.set_description(the_dungeon['description'])
                        embed = discord.Embed(title=f"Welcome to the {dungeon.get_title()}")
                        embed.set_thumbnail(url=the_dungeon['image'])
                        await interaction.followup.send(embed=embed)
                else:
                    await interaction.followup.send("Failed.")
            else:
                await class_selection(interaction=interaction)
        except Exception as e:
            await self.client.send_error_message(e)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Dungeons(client))
