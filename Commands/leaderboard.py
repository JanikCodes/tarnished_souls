import discord
from discord import app_commands
from discord.ext import commands

import db
from Classes.user import User
from Utils.classes import class_selection


def get_leaderboard_text_from_choice(selected_choice, idUser):
    ld_text = str()
    match selected_choice:
        case "runes":
            leaderboard = db.get_leaderboard_runes()
            user_pos = db.get_user_position_in_lb_runes(idUser=idUser)
            ld_text = "**Top 10 players with the highest rune count**\n"

            for x in range(len(leaderboard)):
                ld_text += f"**{x + 1}.** {leaderboard[x][0]} - `{leaderboard[x][1]}` runes\n"
            return ld_text, user_pos
        case "level":
            leaderboard = db.get_leaderboard_levels()
            user_pos = db.get_user_position_in_lb_level(idUser=idUser)
            ld_text = "**Top 10 players with the highest level**\n"

            for x in range(len(leaderboard)):
                ld_text += f"**{x + 1}.** {leaderboard[x][0]} - level `{leaderboard[x][1]}`\n"
            return ld_text, user_pos
        case "wave":
            leaderboard = db.get_leaderboard_horde()
            user_pos = db.get_user_position_in_lb_horde(idUser=idUser)
            ld_text = "**Top 10 players with the highest wave count in horde mode**\n"

            for x in range(len(leaderboard)):
                ld_text += f"**{x + 1}.** {leaderboard[x][0]} - wave `{leaderboard[x][1]}`\n"
            return ld_text, user_pos
        case "inv_kills":
            leaderboard = db.get_leaderboard_invasion()
            user_pos = db.get_user_position_in_lb_invasion(idUser=idUser)
            ld_text = "**Top 10 players with the highest kills for invasions**\n"

            for x in range(len(leaderboard)):
                ld_text += f"**{x + 1}.** {leaderboard[x][0]} - `{leaderboard[x][1]}` kills\n"
            return ld_text, user_pos


    ld_text = "There was an error.."
    return ld_text


class LeaderboardCommand(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="leaderboard", description="Display your runes amount")
    @app_commands.choices(choices=[
        app_commands.Choice(name="Runes", value="runes"),
        app_commands.Choice(name="Level", value="level"),
        app_commands.Choice(name="Horde-mode", value="wave"),
        app_commands.Choice(name="Invasion Kills", value="inv_kills"),
    ])
    async def leaderboard(self, interaction: discord.Interaction, choices: app_commands.Choice[str]):
        try:
            await interaction.response.defer()

            self.client.add_to_activity()

            if db.validate_user(interaction.user.id):

                selected_choice = choices.value
                user = User(interaction.user.id)

                ld_text, pos = get_leaderboard_text_from_choice(selected_choice, user.get_userId())

                embed = discord.Embed(title=f"Leaderboard",
                                      description=ld_text)

                embed.set_footer(text=f"Your position: #{pos}")

                await interaction.followup.send(embed=embed)
            else:
                await class_selection(interaction=interaction)
        except Exception as e:
            await self.client.send_error_message(e)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(LeaderboardCommand(client))
