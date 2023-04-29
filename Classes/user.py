import db

BASE_DAMAGE = 25

lookup_table = {
    1: 300, 2: 304, 3: 312, 4: 322, 5: 334, 6: 347, 7: 362, 8: 378, 9: 396, 10: 414,
    11: 434, 12: 455, 13: 476, 14: 499, 15: 522, 16: 547, 17: 572, 18: 598, 19: 624, 20: 652,
    21: 680, 22: 709, 23: 738, 24: 769, 25: 800, 26: 833, 27: 870, 28: 910, 29: 951, 30: 994,
    31: 1037, 32: 1081, 33: 1125, 34: 1170, 35: 1216, 36: 1262, 37: 1308, 38: 1355, 39: 1402, 40: 1450,
    41: 1476, 42: 1503, 43: 1529, 44: 1555, 45: 1581, 46: 1606, 47: 1631, 48: 1656, 49: 1680, 50: 1704,
    51: 1727, 52: 1750, 53: 1772, 54: 1793, 55: 1814, 56: 1834, 57: 1853, 58: 1871, 59: 1887, 60: 1900,
    61: 1906, 62: 1912, 63: 1918, 64: 1924, 65: 1930, 66: 1936, 67: 1942, 68: 1948, 69: 1954, 70: 1959,
    71: 1965, 72: 1971, 73: 1977, 74: 1982, 75: 1988, 76: 1993, 77: 1999, 78: 2004, 79: 2010, 80: 2015,
    81: 2020, 82: 2026, 83: 2031, 84: 2036, 85: 2041, 86: 2046, 87: 2051, 88: 2056, 89: 2060, 90: 2065,
    91: 2070, 92: 2074, 93: 2078, 94: 2082, 95: 2086, 96: 2090, 97: 2094, 98: 2097, 99: 2100
}


class User:
    def __init__(self, userId=None):
        if userId is not None:
            result = db.get_user_with_id(userId)
            self.userId = result[0]
            self.userName = result[1]
            self.level = result[2]
            self.xp = result[3]
            self.runes = result[4]
            self.vigor = result[5]
            self.mind = result[6]
            self.endurance = result[7]
            self.strength = result[8]
            self.dexterity = result[9]
            self.intelligence = result[10]
            self.faith = result[11]
            self.arcane = result[12]
            self.last_explore = result[13]
            self.weapon = db.get_item_from_user_with_id_rel(idUser=userId, idRel=result[14])
            self.head = db.get_item_from_user_with_id_rel(idUser=userId, idRel=result[15])
            self.chest = db.get_item_from_user_with_id_rel(idUser=userId, idRel=result[16])
            self.legs = db.get_item_from_user_with_id_rel(idUser=userId, idRel=result[17])
            self.gauntlet = db.get_item_from_user_with_id_rel(idUser=userId, idRel=result[18])

            self.current_location = db.get_location_from_id(idLocation=result[19])
            self.max_location = db.get_location_from_id(idLocation=result[20])
            self.ng = result[21]
            self.last_quest = result[22]

            self.health = self.get_max_health()
            self.stamina = self.get_max_stamina()
            self.remaining_flasks = result[23]
            self.dodge_next = False
        else:
            # empty constructor
            pass

    def update_user(self):
        result = db.get_user_with_id(self.userId)
        self.userId = result[0]
        self.userName = result[1]
        self.level = result[2]
        self.xp = result[3]
        self.runes = result[4]
        self.vigor = result[5]
        self.mind = result[6]
        self.endurance = result[7]
        self.strength = result[8]
        self.dexterity = result[9]
        self.intelligence = result[10]
        self.faith = result[11]
        self.arcane = result[12]
        self.last_explore = result[13]
        self.weapon = db.get_item_from_user_with_id_rel(idUser=self.userId, idRel=result[14])
        self.head = db.get_item_from_user_with_id_rel(idUser=self.userId, idRel=result[15])
        self.chest = db.get_item_from_user_with_id_rel(idUser=self.userId, idRel=result[16])
        self.legs = db.get_item_from_user_with_id_rel(idUser=self.userId, idRel=result[17])
        self.gauntlet = db.get_item_from_user_with_id_rel(idUser=self.userId, idRel=result[18])

        self.health = self.get_max_health()
        self.stamina = self.get_max_stamina()
        self.remaining_flasks = result[23]
        self.dodge_next = False

        return self

    def get_ng(self):
        return self.ng

    def get_last_quest(self):
        return self.last_quest

    # getters
    def get_userId(self):
        return self.userId

    def get_userName(self):
        return self.userName

    def get_level(self):
        return self.level

    def get_xp(self):
        return self.xp

    def get_runes(self):
        return self.runes

    def get_vigor(self):
        return self.vigor

    def get_mind(self):
        return self.mind

    def get_endurance(self):
        return self.endurance

    def get_strength(self):
        return self.strength

    def get_dexterity(self):
        return self.dexterity

    def get_intelligence(self):
        return self.intelligence

    def get_faith(self):
        return self.faith

    def get_arcane(self):
        return self.arcane

    def get_last_explore(self):
        return self.last_explore

    def get_weapon(self):
        return self.weapon

    def get_head(self):
        return self.head

    def get_chest(self):
        return self.chest

    def get_legs(self):
        return self.legs

    def get_all_stat_levels(self):
        return self.strength + self.endurance + self.faith + self.vigor + self.intelligence + self.arcane + self.dexterity + self.mind

    def set_userId(self, userId):
        self.userId = userId

    def set_userName(self, userName):
        self.userName = userName

    def set_level(self, level):
        self.level = level

    def set_xp(self, xp):
        self.xp = xp

    def set_runes(self, runes):
        self.runes = runes

    def set_vigor(self, vigor):
        self.vigor = vigor

    def set_mind(self, mind):
        self.mind = mind

    def set_endurance(self, endurance):
        self.endurance = endurance

    def set_strength(self, strength):
        self.strength = strength

    def set_dexterity(self, dexterity):
        self.dexterity = dexterity

    def set_intelligence(self, intelligence):
        self.intelligence = intelligence

    def set_faith(self, faith):
        self.faith = faith

    def set_arcane(self, arcane):
        self.arcane = arcane

    def set_last_explore(self, last_explore):
        self.last_explore = last_explore

    def set_weapon(self, e_weapon):
        self.weapon = db.get_item_from_user_with_id_rel(idUser=self.get_userId(), idRel=e_weapon)

    def set_head(self, e_head):
        self.head = db.get_item_from_user_with_id_rel(idUser=self.get_userId(), idRel=e_head)

    def set_chest(self, e_chest):
        self.chest = db.get_item_from_user_with_id_rel(idUser=self.get_userId(), idRel=e_chest)

    def set_legs(self, e_legs):
        self.legs = db.get_item_from_user_with_id_rel(idUser=self.get_userId(), idRel=e_legs)

    def get_is_required_for_item(self, item):
        if self.get_vigor() < item.get_reqVigor():
            return False
        if self.get_mind() < item.get_reqMind():
            return False
        if self.get_endurance() < item.get_reqEndurance():
            return False
        if self.get_strength() < item.get_reqStrength():
            return False
        if self.get_dexterity() < item.get_reqDexterity():
            return False
        if self.get_intelligence() < item.get_reqIntelligence():
            return False
        if self.get_faith() < item.get_reqFaith():
            return False
        if self.get_arcane() < item.get_reqArcane():
            return False

        return True

    def get_health(self):
        return self.health

    def get_remaining_flasks(self):
        return self.remaining_flasks

    def get_max_health(self):
        return lookup_table[self.vigor] if self.vigor in lookup_table else None

    def reduce_health(self, amount):
        armor = int((self.get_total_armor() / 4))
        absorb = min(amount - armor, 15)

        self.health = max(self.health - (amount - absorb), 0)

    def increase_health(self, amount):
        if self.remaining_flasks > 0:
            self.health = min(self.health + amount, self.get_max_health())
            self.remaining_flasks = max(self.remaining_flasks - 1, 0)

    def get_damage(self):
        if self.weapon is not None:
            return BASE_DAMAGE + self.weapon.get_total_value(self)
        else:
            return BASE_DAMAGE

    def get_total_weight(self):
        weight = 0
        if self.weapon:
            weight += self.weapon.get_weight()
        if self.head:
            weight += self.head.get_weight()
        if self.chest:
            weight += self.chest.get_weight()
        if self.legs:
            weight += self.legs.get_weight()
        if self.gauntlet:
            weight += self.gauntlet.get_weight()

        return weight

    def reduce_stamina(self, amount):
        self.stamina = max(self.stamina - amount, 0)

    def increase_stamina(self, amount):
        self.stamina = min(self.stamina + amount, self.get_max_stamina())

    def get_max_stamina(self):
        value = self.endurance
        if value >= 1 and value <= 15:
            return max(int(80 + 25 * ((value - 1) / 14)) - self.get_total_weight(), 0)
        elif value >= 16 and value <= 35:
            return max(int(105 + 25 * ((value - 15) / 15)) - self.get_total_weight(), 0)
        elif value >= 36 and value <= 60:
            return max(int(130 + 25 * ((value - 30) / 20)) - self.get_total_weight(), 0)
        elif value >= 61 and value <= 99:
            return max(int(155 + 15 * ((value - 50) / 49)) - self.get_total_weight(), 0)
        else:
            return 0  # return 0 for invalid endurance value

    def get_stamina(self):
        return self.stamina

    def dodge(self, amount):
        if self.stamina - amount >= 0:
            self.reduce_stamina(amount)
            self.dodge_next = True

    def get_is_dodging(self):
        return self.dodge_next

    def reset_dodge(self):
        self.dodge_next = False

    def get_total_armor(self):
        armor = 0
        if self.head:
            armor += self.head.get_total_value(self)
        if self.chest:
            armor += self.chest.get_total_value(self)
        if self.legs:
            armor += self.legs.get_total_value(self)
        if self.gauntlet:
            armor += self.gauntlet.get_total_value(self)

        return armor

    def has_item_equipped(self, item):
        if self.weapon:
            if self.weapon.get_idRel() == item.get_idRel():
                return True
        if self.head:
            if self.head.get_idRel() == item.get_idRel():
                return True
        if self.chest:
            if self.chest.get_idRel() == item.get_idRel():
                return True
        if self.legs:
            if self.legs.get_idRel() == item.get_idRel():
                return True
        if self.gauntlet:
            if self.gauntlet.get_idRel() == item.get_idRel():
                return True

        return False

    def get_gauntlet(self):
        return self.gauntlet

    def get_max_location(self):
        return self.max_location

    def get_current_location(self):
        return self.current_location