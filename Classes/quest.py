import db
from Classes.enemy import Enemy


class Quest:
    def __init__(self, id=None, title=None, description=None, req_kills=None, req_item_count=None, req_runes=None, idItem=None, idEnemy=None, runeReward=None,\
                 locationIdReward=None, req_explore_count=None, explore_location=None, cooldown=None):
        if id is not None:
            self.id = id
            self.title = title
            self.description = description
            self.req_kills = req_kills
            self.req_item_count = req_item_count
            self.req_runes = req_runes
            self.req_item = db.get_item_from_item_id(idItem)
            self.req_enemy = Enemy(idEnemy) if idEnemy is not None else None
            self.rune_reward = runeReward
            self.item_reward = db.get_quest_item_reward(idQuest=id)
            self.location_reward = db.get_location_from_id(locationIdReward)
            self.req_explore_count = req_explore_count
            self.explore_location = db.get_location_from_id(explore_location)
            self.cooldown = cooldown

        else:
            # empty constructor
            self.item_reward = []
            pass

    def get_id(self):
        return self.id

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

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

    def get_item_reward(self):
        return self.item_reward

    def get_location_reward(self):
        return self.location_reward

    def get_req_explore_count(self):
        return self.req_explore_count

    def get_explore_location(self):
        return self.explore_location

    def get_cooldown(self):
        return self.cooldown

    def set_id(self, id):
        self.id = id

    def set_title(self, title):
        self.title = title

    def set_description(self, description):
        self.description = description

    def set_req_kills(self, req_kills):
        self.req_kills = req_kills

    def set_req_item_count(self, req_item_count):
        self.req_item_count = req_item_count

    def set_req_runes(self, req_runes):
        self.req_runes = req_runes

    def set_req_item(self, req_item):
        self.req_item = req_item

    def set_req_enemy(self, req_enemy_id):
        self.req_enemy = Enemy(idEnemy=req_enemy_id) if req_enemy_id is not None else None

    def set_rune_reward(self, rune_reward):
        self.rune_reward = rune_reward

    def set_item_reward(self, item):
        self.item_reward.append(item)

    def set_location_reward(self, location_reward_id):
        self.location_reward = db.get_location_from_id(location_reward_id)

    def set_req_explore_count(self, req_explore_count):
        self.req_explore_count = req_explore_count

    def set_explore_location(self, explore_location_id):
        self.explore_location = db.get_location_from_id(explore_location_id)

    def set_cooldown(self, cooldown):
        self.cooldown = cooldown

