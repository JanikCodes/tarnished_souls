import db


class Dungeon:
    def __init__(self, id=None):
        if id is not None:
            self.__id = id
            load_dungeon = db.load_dungeon(idDungeon=id)
            self.__title = load_dungeon[0]
            self.__description = load_dungeon[1]
            self.__loot_table = load_dungeon[2]
            self.__encounters = load_dungeon[3]
        else:
            pass

    def __get_id(self):
        return self.__id

    def get_title(self):
        return self.__title

    def get_description(self):
        return self.__description

    def get_loot_table(self):
        return self.__loot_table

    def get_encounters(self):
        return self.__encounters

    def set_id(self, id):
        self.__id = id

    def set_title(self, title):
        self.__title = title

    def set_description(self, description):
        self.__description = description

    def set_loot_table(self, loot_table):
        self.__loot_table = loot_table

    def set_encounters(self, encounters):
        self.__encounters = encounters
