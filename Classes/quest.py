import db
from Classes.enemy import Enemy


class Quest:
    def __init__(self, id, title, description, req_kills, req_item_count, req_runes, idItem, idEnemy):
        self.id = id
        self.title = title
        self.description = description
        self.req_kills = req_kills
        self.req_item_count = req_item_count
        self.req_runes = req_runes
        self.req_item = db.get_item_from_item_id(idItem)
        self.req_enemy = Enemy(idEnemy)

    def get_id(self):
        return self.id

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
