import discord

import db


class QuestProgress:
    def __init__(self, idRel, idQuest, idUser, remaining_kills, remaining_item_count, remaining_runes, remaining_explore_count):
        self.idRel = idRel
        self.quest = db.get_quest_with_id(idQuest=idQuest)
        self.idUser = idUser
        self.remaining_kills = remaining_kills
        self.remaining_item_count = remaining_item_count
        self.remaining_runes = remaining_runes
        self.remaining_explore_count = remaining_explore_count

    def get_idRel(self):
        return self.idRel

    def get_quest(self):
        return self.quest

    def get_remaining_kills(self):
        return self.remaining_kills

    def get_remaining_item_count(self):
        return self.remaining_item_count

    def get_remaining_runes(self):
        return self.remaining_runes

    def get_remaining_explore_count(self):
        return self.remaining_explore_count

    def get_quest_progress_text(self):
        text = str()

        if self.quest.req_item_count:
            if self.quest.req_item_count > 0:
                remaining = self.quest.get_req_item_count() - self.remaining_item_count
                text += f"**Collect** `{self.quest.req_item.get_name()}` **{remaining}/{self.quest.get_req_item_count()}**\n{self.quest.req_item.get_dropped_from_enemies_text()}"
        if self.quest.req_kills:
            if self.quest.req_kills > 0:
                remaining = self.quest.get_req_kills() - self.remaining_kills
                text += f"**Defeat** `{self.quest.req_enemy.get_name()}` in `{self.quest.req_enemy.get_location().get_name()}` **{remaining}/{self.quest.get_req_kills()}** \n"
        if self.quest.req_runes:
            if self.quest.req_runes > 0:
                remaining = self.quest.get_req_runes() - self.remaining_runes
                text += f"**Earn** `runes` **{remaining}/{self.quest.get_req_runes()}** \n"
        if self.quest.req_explore_count:
            if self.quest.req_explore_count > 0:
                remaining = self.quest.get_req_explore_count() - self.remaining_explore_count
                text += f"**Explore** `{self.quest.get_explore_location().get_name()}` **{remaining}/{self.quest.get_req_explore_count()}** \n"

        return text

    def has_rewards(self):
        return self.quest.get_rune_reward() > 0 or self.quest.get_location_reward() or len(self.quest.get_item_reward()) > 0

    def get_quest_reward_text(self, interaction):
        text = str()

        if self.quest.get_rune_reward() > 0:
            text += f"- `{self.quest.get_rune_reward()}` runes!\n"
        if self.quest.get_location_reward():
            text += f"- `{self.quest.get_location_reward().get_name()}` as a new location!\n"
        if len(self.quest.get_item_reward()) > 0:
            for item in self.quest.get_item_reward():
                category_emoji = discord.utils.get(interaction.client.get_guild(763425801391308901).emojis, name=item.get_iconCategory())
                text += f"- {category_emoji} `{item.get_name()}` **{item.get_count()}**x\n"

        return text

    def is_finished(self):
        return self.remaining_runes == 0 and self.remaining_kills == 0 and self.remaining_item_count == 0 and self.remaining_explore_count == 0