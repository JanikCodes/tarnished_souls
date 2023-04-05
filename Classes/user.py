import db

class User:
    def __init__(self, userId = None):
        if userId is not None:
            result = db.get_user_with_id(userId)
            self.userId = result[0]
            self.userName = result[1]
            self.level = result[2]
            self.xp = result[3]
            self.souls = result[4]
            self.vigor = result[5]
            self.mind = result[6]
            self.endurance = result[7]
            self.strength = result[8]
            self.dexterity = result[9]
            self.intelligence = result[10]
            self.faith = result[11]
            self.arcane = result[12]
            self.last_explore = result[13]
            self.e_head = result[14]
            self.e_chest = result[15]
            self.e_legs = result[16]
        else:
            # empty constructor
            pass

    def update_user(self):
        return User(self.userId)

    # getters
    def get_userId(self):
        return self.userId

    def get_userName(self):
        return self.userName

    def get_level(self):
        return self.level

    def get_xp(self):
        return self.xp

    def get_souls(self):
        return self.souls

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

    def get_e_weapon(self):
        return self.e_weapon

    def get_e_head(self):
        return self.e_head

    def get_e_chest(self):
        return self.e_chest

    def get_e_legs(self):
        return self.e_legs

    # customs
    def get_all_stat_levels(self):
        return self.strength + self.endurance + self.faith + self.vigor + self.intelligence + self.arcane + self.dexterity + self.mind
    # setters
    def set_userId(self, userId):
        self.userId = userId

    def set_userName(self, userName):
        self.userName = userName

    def set_level(self, level):
        self.level = level

    def set_xp(self, xp):
        self.xp = xp

    def set_souls(self, souls):
        self.souls = souls

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

    def set_e_weapon(self, e_weapon):
        self.e_weapon = e_weapon

    def set_e_head(self, e_head):
        self.e_head = e_head

    def set_e_chest(self, e_chest):
        self.e_chest = e_chest

    def set_e_legs(self, e_legs):
        self.e_legs = e_legs

    def get_is_required_for_item(self, item):
        return self.get_vigor() >= item.get_reqVigor() & self.get_mind() >= item.get_reqMind() & self.get_endurance() >= item.get_reqEndurance() & self.get_strength() >= item.get_reqStrength() & self.get_dexterity() >= item.get_reqDexterity() & self.get_intelligence() >= item.get_reqIntelligence() & self.get_faith() >= item.get_reqFaith() & self.get_arcane() >= item.get_reqArcane()