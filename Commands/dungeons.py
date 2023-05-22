import discord
from discord import app_commands
from discord.ext import commands

import db
from Classes.user import User
from Classes.dungeon import Dungeon
from Utils.classes import class_selection


class Dungeons(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="dungeons", description="Explore available dungeons and earn items!")
    async def dungeons(self, interaction: discord.Interaction):
        if not interaction or interaction.is_expired():
            return

        try:
            await interaction.response.defer()

            self.client.add_to_activity()

            if db.validate_user(interaction.user.id):
                user = User(interaction.user.id)
                dungeon = Dungeon()
                dungeon.set_id(1)
                dungeon.set_title("Miner's Paradise")
                dungeon.set_description("This is the first dungeon to come to life!")
                loot_table = ["Item1", "Item2"]
                dungeon.set_loot_table(loot_table)

                encounter_list = ["Encounter1", "Encounter2"]
                dungeon.set_encounters(encounter_list)

                embed = discord.Embed(title=f"Welcome to the {dungeon.get_title()}")
                description = "Available encounters: "
                for encounter in dungeon.get_encounters():
                    description += f"{encounter} "

                for item in dungeon.get_loot_table():
                    embed.add_field(name=item, value="item_name")

                await interaction.followup.send(embed=embed)
            else:
                await class_selection(interaction=interaction)
        except Exception as e:
            await self.client.send_error_message(e)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Dungeons(client))
