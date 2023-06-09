import db


class Location:
    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description
        self.item_rewards = db.get_items_from_location_id(idLocation=id)

        self.items = []

    def get_id(self):
        return self.id

    def get_description(self):
        return self.description

    def get_name(self):
        return self.name

    def get_item_rewards(self):
        return self.item_rewards

    def get_items(self):
        return self.items

    def add_item_reward(self, item):
        self.items.append(item)
