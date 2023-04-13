import db


class QuestProgress:
    def __init__(self, idRel, idQuest, idUser, remaining_kills, remaining_item_count, remaining_runes):
        self.idRel = idRel
        self.quest = db.get_quest_with_id(idQuest=idQuest)
        self.idUser = idUser
        self.remaining_kills = remaining_kills
        self.remaining_item_count = remaining_item_count
        self.remaining_runes = remaining_runes

    def get_idRel(self):
        return self.idRel

    def get_quest(self):
        return self.quest

    def get_remaining_kills(self):
        return self.remaining_kills

    def get_remaining_item_count(self):
        return self.remaining_item_count

    def get_remaining_runes(self):
        return self.get_remaining_runes()

    def get_quest_progress_text(self):
        text = str()

        if self.quest.req_item_count > 0:
            remaining = self.quest.req_item_count - self.remaining_item_count
            text += f"**Collect** `{self.quest.req_item.get_name()}` {remaining}/{self.quest.req_item_count} \n"
        if self.quest.req_kills > 0:
            remaining = self.quest.req_kills - self.remaining_kills
            text += f"**Defeat** `{self.quest.req_enemy.get_name()}` {remaining}/{self.quest.req_kills} \n"
        if self.quest.req_runes > 0:
            remaining = self.quest.req_runes - self.remaining_runes
            text += f"**Earn** `runes` {remaining}/{self.quest.req_runes}"

        return text
