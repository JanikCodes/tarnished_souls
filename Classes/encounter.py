import db


class Encounter:
    def __init__(self, id = None, description = None, drop_rate = None, idLocation = None):
        if id is not None:
            self.id = id
            self.description = description
            self.drop_rate = drop_rate
            self.location = db.get_location_from_id(idLocation=idLocation)
            self.item_rewards = []

        else:
            # empty constructor
            self.location = None
            self.item_rewards = []


    def get_id(self):
        return self.id

    def get_description(self):
        return self.description

    def get_drop_rate(self):
        return self.drop_rate

    def get_location(self):
        return self.location

    def set_id(self, id):
        self.id = id

    def set_description(self, description):
        self.description = description

    def set_drop_rate(self, drop_rate):
        self.drop_rate = drop_rate

    def set_location(self, location):
        self.location = location

    def set_item_rewards(self, item):
        self.item_rewards.append(item)

    def get_item_rewards(self):
        return self.item_rewards