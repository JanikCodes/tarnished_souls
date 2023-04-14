import db


class Encounter:
    def __init__(self, id, description, drop_rate, idLocation):
        self.id = id
        self.description = description
        self.drop_rate = drop_rate
        self.location = db.get_location_from_id(idLocation=idLocation)

    def get_id(self):
        return self.id

    def get_description(self):
        return self.description

    def get_drop_rate(self):
        return self.drop_rate
