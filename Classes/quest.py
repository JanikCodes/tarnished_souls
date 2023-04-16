import db
from Classes.enemy import Enemy


class Quest:
    def __init__(self, id, title, description, req_kills, req_item_count, req_runes, idItem, idEnemy, runeReward, locationIdReward, req_explore_count, explore_location, cooldown):
        self.id = id
        self.title = title
        self.description = description
        self.req_kills = req_kills
        self.req_item_count = req_item_count
        self.req_runes = req_runes
        self.req_item = db.get_item_from_item_id(idItem)
        self.req_enemy = Enemy(idEnemy) if idEnemy is not None else None
        self.rune_reward = runeReward
        self.item_reward = db.get_quest_item_reward(idQuest = id)
        self.location_reward = db.get_location_from_id(locationIdReward)
        self.req_explore_count = req_explore_count
        self.explore_location = db.get_location_from_id(explore_location)
        self.cooldown = cooldown

    def get_id(self):
        return self.id

    def get_cooldown(self):
        return self.cooldown

    def get_item_reward(self):
        return self.item_reward

    def get_req_explore_count(self):
        return self.req_explore_count

    def get_explore_location(self):
        return self.explore_location

    def get_description(self):
        return self.description

    def get_title(self):
        return self.title

    def get_req_kills(self):
        return self.req_kills

    def get_req_item_count(self):
        return self.req_item_count

    def get_req_runes(self):
        return self.req_runes

    def get_item(self):
        return self.req_item

    def get_enemy(self):
        return self.req_enemy

    def get_rune_reward(self):
        return self.rune_reward

    def get_location_reward(self):
        return self.location_reward