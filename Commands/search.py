import time

import discord
from discord import app_commands
from discord.ext import commands

import config
import db
from Classes.user import User
from Utils.classes import class_selection

MAX_ITEM_FOR_PAGE = 1


class SearchResultsPageButton(discord.ui.Button):
    def __init__(self, text, direction, user, func, last_page, total_page_count, last_filter):
        super().__init__(label=text, style=discord.ButtonStyle.primary, disabled=False)
        self.direction = direction
        self.func = func
        self.user = user
        self.last_page = last_page
        self.total_page_count = total_page_count
        self.last_filter = last_filter

        if direction == 'prev':
            if last_page == 1:
                self.disabled = True
        elif direction == 'next':
            if total_page_count == last_page:
                self.disabled = True
            if total_page_count == 0:
                self.disabled = True

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != int(self.user.get_userId()):
            embed = discord.Embed(title=f"You're not allowed to use this action!",
                                  description="",
                                  colour=discord.Color.red())
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        await interaction.response.defer()

        if self.direction == 'next':
            await view_search_results_page(interaction=interaction, user=self.user, page=self.last_page + 1, label=self.func,
                                           filter=self.last_filter)
        elif self.direction == 'prev':
            await view_search_results_page(interaction=interaction, user=self.user, page=self.last_page - 1, label=self.func,
                                           filter=self.last_filter)
            pass


class SearchResultsView(discord.ui.View):
    def __init__(self, user, current_page, func, total_page_count, last_filter):
        super().__init__()
        self.user = user.update_user()
        self.add_item(
            SearchResultsPageButton(text="Previous", direction="prev", user=user, last_page=current_page, func=func,
                                    total_page_count=total_page_count, last_filter=last_filter))
        self.add_item(SearchResultsPageButton(text="Next", direction="next", user=user, last_page=current_page, func=func,
                                              total_page_count=total_page_count, last_filter=last_filter))


async def view_search_results_page(interaction, user, page, label, filter=None):
    searches = db.search_with_name(idUser=user.get_userId(), name=label, filter=filter, page=page, max_page=MAX_ITEM_FOR_PAGE)[0]
    searches_count = db.search_with_name(idUser=user.get_userId(), name=label, filter=filter, page=page, max_page=MAX_ITEM_FOR_PAGE)[1]

    new_embed = discord.Embed(title=f"Searching for `{label}`..",
                              description="Below are your search results.")
    new_embed.colour = discord.Color.brand_green()

    total_page_count = (int(searches_count) + MAX_ITEM_FOR_PAGE - 1) // MAX_ITEM_FOR_PAGE

    if searches:
        equipped_emoji = discord.utils.get(
            interaction.client.get_guild(config.botConfig["hub-server-guild-id"]).emojis,
            name='equipped')

        fav_emoji = discord.utils.get(
            interaction.client.get_guild(config.botConfig["hub-server-guild-id"]).emojis,
            name='favorite')

        match filter:
            case "enemy":
                for enemy in searches:
                    description = "" if enemy.get_description().upper() != "BOSS" else f"\n💀 {enemy.get_description().capitalize()}"
                    new_embed.add_field(name="Name:", value=f"`{enemy.get_name()}{description}`")
                    new_embed.add_field(name="Found in:", value=f"`{enemy.get_location().get_name()}`")

                    item_drops = str()
                    for item in enemy.get_item_rewards():
                        item_drops += f"\n`{item.get_name()}` with a **{item.get_drop_rate()}%** drop chance!"

                        user_item = db.does_item_exist_for_user(idUser=user.get_userId(), item=item)

                        if user_item:
                            item_drops += f" {equipped_emoji}"
                            item_drops += f" {fav_emoji}" if user_item.get_favorite() == 1 else ""

                    if item_drops != "":
                        new_embed.add_field(name="Drops:", value=item_drops, inline=False)
            case "inventory":
                for item in searches:
                    new_embed.set_thumbnail(url=item.get_icon_url())

                    item_level = str() if item.get_level() == 0 else f"**+{item.get_level()}**"

                    eq_text = equipped_emoji if user.has_item_equipped(item) else str()

                    item_name = f"{item.get_name()} {item_level} `ID: {item.get_idRel()}` {eq_text}"
                    if item.get_favorite() == 1:
                        item_name += f" {fav_emoji}"

                    new_embed.add_field(name="Name:", value=item_name)
                    new_embed.add_field(name="Amount owned:", value=f"{item.get_count()}x")
                    new_embed.add_field(name="", value="", inline=False) # placeholder

                    locations = str()
                    for location in db.get_all_locations():
                        if location.get_item_rewards() is None:
                            continue
                        for location_item in location.get_item_rewards():
                            if item.get_idItem() == location_item.get_idItem():
                                locations += f"\n{location.get_name()}" if location.get_name() not in locations else ""

                    if locations != "":
                        new_embed.add_field(name="Found in:", value=locations)
                    new_embed.add_field(name="Sells for:", value=f"**{item.get_price()}** runes.")
                    new_embed.add_field(name="", value="", inline=False)  # placeholder

                    if item.get_item_type().upper() == "WEAPON":
                        extra_val_text = str() if item.get_extra_value() == 0 else f"(*+{item.get_extra_value()}*)"

                        new_embed.add_field(
                            name=f"**Statistics:**",
                            value=f"`Damage:` **{item.get_value_with_scaling(user)}** {extra_val_text}`Weight:` **{item.get_weight()}**\n"
                                  f"**Requirements:** \n"
                                  f"{item.get_requirement_text()}\n"
                                  f"**Scaling:** \n"
                                  f"{item.get_scaling_text()}",
                            inline=False)

                    if item.get_item_type().upper() == "ARMOR":
                        extra_val_text = str() if item.get_extra_value() == 0 else f"(*+{item.get_extra_value()}*)"
                        
                        new_embed.add_field(
                            name=f"**Statistics:**",
                            value=f"`Armor:` **{item.get_value_with_scaling(user)}** {extra_val_text} `Weight:` **{item.get_weight()}**\n",
                            inline=False)

                    dropped_enemy = str()
                    for enemy in db.get_all_enemies():
                        if enemy.get_item_rewards() is None:
                            continue
                        for enemy_item in enemy.get_item_rewards():
                            if item.get_idItem() == enemy_item.get_idItem():
                                dropped_enemy += f"\n**{enemy.get_name()}** with a **{enemy_item.get_drop_rate()}%** drop chance!"

                    if dropped_enemy != "":
                        new_embed.add_field(name="Dropped by:", value=dropped_enemy, inline=False)

            case "item":
                for item in searches:
                    new_embed.set_thumbnail(url=item.get_icon_url())
                    user_item = db.does_item_exist_for_user(idUser=user.get_userId(), item=item)

                    item_name = f"{item.get_name()}"

                    new_embed.add_field(name="Name:", value=item_name)

                    if item.get_item_type().upper() == "WEAPON":
                        extra_val_text = str() if item.get_extra_value() == 0 else f"(*+{item.get_extra_value()}*)"

                        stats_value = (f"`Damage:` **{item.get_value_with_scaling(user)}** {extra_val_text}`Weight:` **{item.get_weight()}**\n"
                                  f"**Requirements:** \n"
                                  f"{item.get_requirement_text()}\n"
                                  f"**Scaling:** \n"
                                  f"{item.get_scaling_text()}")

                        if user_item:
                            level_text = str() if item.get_level() == 0 else f"**+{user_item.get_level()}"

                            eq_text = equipped_emoji if user.has_item_equipped(user_item) else str()

                            fav_text = fav_emoji if user_item.get_favorite() == 1 else str()

                            stats_name = f"__{user_item.get_count()}x {item.get_name()}__ {level_text} `id: {user_item.get_idRel()}` {eq_text} {fav_text}"
                            stats_value = f"**Statistics:**\n{stats_value}"
                        else:
                            stats_name=f"**Statistics:**"

                        new_embed.add_field(name=stats_name, value=stats_value, inline=False)

                    if item.get_item_type().upper() == "ARMOR":
                        extra_val_text = str() if item.get_extra_value() == 0 else f"(*+{item.get_extra_value()}*)"
                        new_embed.add_field(
                            name=f"**Statistics:**",
                            value=f"`Armor:` **{item.get_value_with_scaling(user)}** {extra_val_text} `Weight:` **{item.get_weight()}**\n",
                            inline=False)

                    dropped_enemy = str()
                    for enemy in db.get_all_enemies():
                        if enemy.get_item_rewards() is None:
                            continue
                        for enemy_item in enemy.get_item_rewards():
                            if item.get_idItem() == enemy_item.get_idItem():
                                dropped_enemy += f"\n**{enemy.get_name()}** with a **{enemy_item.get_drop_rate()}%** drop chance!"

                    if dropped_enemy != "":
                        new_embed.add_field(name="Dropped by:", value=dropped_enemy, inline=False)

                    if user_item:
                        new_embed.add_field(name="Currently in Inventory:", value=equipped_emoji)
                    else:
                        new_embed.add_field(name="Currently in Inventory:", value="❌")

    else:
        failed_txt = f"The prompt `{label}` resulted in failure, please check the spelling\nor your filter `Inventory/Enemy/Item`."
        failed_embed=discord.Embed(title="I wasn't able to find anything..", description=failed_txt, colour=discord.Color.red())
        await interaction.followup.send(embed=failed_embed)
        return

    new_embed.set_footer(text=f"Page {page}/{str(total_page_count)}")

    if interaction.message:
        await interaction.message.edit(embed=new_embed, view=SearchResultsView(user=user, current_page=page,
                                                                               total_page_count=total_page_count,
                                                                               last_filter=filter, func=label))
    else:
        await interaction.followup.send(embed=new_embed, view=SearchResultsView(user=user, current_page=page,
                                                                               total_page_count=total_page_count,
                                                                               last_filter=filter, func=label))


class Search(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="search", description="Search for something!")
    @app_commands.describe(prompt="Input a searching prompt.")
    @app_commands.choices(choices=[
        app_commands.Choice(name="Inventory", value="inventory"),
        app_commands.Choice(name="Enemy", value="enemy"),
        app_commands.Choice(name="Item", value="item")
    ])
    async def runes(self, interaction: discord.Interaction, choices: app_commands.Choice[str], prompt: str):
        if not interaction or interaction.is_expired():
            return

        try:
            await interaction.response.defer()

            self.client.add_to_activity()

            if db.validate_user(interaction.user.id):
                await view_search_results_page(interaction=interaction, user=User(interaction.user.id), label=prompt.replace("'", ""), page=1,
                                               filter=choices.value)
            else:
                await class_selection(interaction=interaction)
        except Exception as e:
            await self.client.send_error_message(e)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Search(client))
