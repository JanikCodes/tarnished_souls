import db


class Dungeon:
    def __init__(self, id=None):
        if id is not None:
            self.id = id
            load_dungeon = db.load_dungeon(idDungeon=id)
            self.title = load_dungeon[0]
            self.description = load_dungeon[1]
            self.loot_table = load_dungeon[2]
            self.encounters = load_dungeon[3]
        else:
            pass

    def get_id(self):
        return self.id

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_loot_table(self):
        return self.loot_table

    def get_encounters(self):
        return self.encounters

    def set_id(self, id):
        self.id = id

    def set_title(self, title):
        self.title = title

    def set_description(self, description):
        self.description = description

    def set_loot_table(self, loot_table):
        self.loot_table = loot_table

    def set_encounters(self, encounters):
        self.encounters = encounters
