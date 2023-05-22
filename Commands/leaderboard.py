import discord
from discord import app_commands
from discord.ext import commands

import db
from Classes.user import User
from Utils.classes import class_selection


def convert_to_server_only(bot, interaction, leaderboard):
    server_lb = []
    guild = bot.client.get_guild(interaction.guild_id)
    if guild is None:
        print("Warning: Guild in Leaderboard was None in 'convert_to_server_only'")
        return server_lb

    for lb_value in leaderboard:
        user = guild.get_member(int(lb_value[2]))
        # User exists in that server
        if user:
            server_lb.append(lb_value)

    return server_lb

def get_position_in_leaderboard(leaderboard, idUser):
    for index, sublist in enumerate(leaderboard):
        if len(sublist) >= 3 and sublist[2] == idUser:
            return index + 1
    return -1

def limit_leaderboard(leaderboard, amount):
    return leaderboard[:amount]

def get_leaderboard_text_from_choice(bot, interaction, selected_range, selected_choice, idUser):
    ld_text = str()
    match selected_choice:
        case "runes":
            leaderboard = db.get_leaderboard_runes()
            if selected_range == 'server':
                leaderboard = convert_to_server_only(bot,interaction, leaderboard)

            user_pos = get_position_in_leaderboard(leaderboard, idUser)

            leaderboard = limit_leaderboard(leaderboard, 10)

            ld_text = "**Top 10 players with the highest rune count**\n"

            for x in range(len(leaderboard)):
                ld_text += f"**{x + 1}.** {leaderboard[x][0]} - `{leaderboard[x][1]}` runes\n"
            return ld_text, user_pos
        case "level":
            leaderboard = db.get_leaderboard_levels()
            if selected_range == 'server':
                leaderboard = convert_to_server_only(bot,interaction, leaderboard)

            user_pos = get_position_in_leaderboard(leaderboard, idUser)
            leaderboard = limit_leaderboard(leaderboard, 10)

            ld_text = "**Top 10 players with the highest level**\n"

            for x in range(len(leaderboard)):
                ld_text += f"**{x + 1}.** {leaderboard[x][0]} - level `{leaderboard[x][1]}`\n"
            return ld_text, user_pos
        case "wave":
            leaderboard = db.get_leaderboard_horde()
            if selected_range == 'server':
                leaderboard = convert_to_server_only(bot,interaction, leaderboard)

            user_pos = get_position_in_leaderboard(leaderboard, idUser)
            leaderboard = limit_leaderboard(leaderboard, 10)

            ld_text = "**Top 10 players with the highest wave count in horde mode**\n"

            for x in range(len(leaderboard)):
                ld_text += f"**{x + 1}.** {leaderboard[x][0]} - wave `{leaderboard[x][1]}`\n"
            return ld_text, user_pos
        case "inv_kills":
            leaderboard = db.get_leaderboard_invasion()
            if selected_range == 'server':
                leaderboard = convert_to_server_only(bot,interaction, leaderboard)

            user_pos = get_position_in_leaderboard(leaderboard, idUser)
            leaderboard = limit_leaderboard(leaderboard, 10)

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
    @app_commands.choices(type=[
        app_commands.Choice(name="Runes", value="runes"),
        app_commands.Choice(name="Level", value="level"),
        app_commands.Choice(name="Horde-mode", value="wave"),
        app_commands.Choice(name="Invasion Kills", value="inv_kills"),
    ])
    @app_commands.choices(range=[
        app_commands.Choice(name="Global", value="global"),
        app_commands.Choice(name="Server", value="server")
    ])
    @app_commands.checks.has_permissions(manage_messages=True, embed_links=True, add_reactions=True,
                                         external_emojis=True, read_message_history=True, read_messages=True,
                                         send_messages=True, use_application_commands=True, use_external_emojis=True)
    async def leaderboard(self, interaction: discord.Interaction, type: app_commands.Choice[str], range: app_commands.Choice[str]):
        if not interaction or interaction.is_expired():
            return

        try:
            await interaction.response.defer()

            self.client.add_to_activity()

            if db.validate_user(interaction.user.id):

                selected_choice = type.value
                user = User(interaction.user.id)

                selected_range = range.value
                ld_text, pos = get_leaderboard_text_from_choice(self, interaction, selected_range, selected_choice, user.get_userId())

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
