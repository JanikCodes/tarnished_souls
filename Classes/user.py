import db


class User:

    userName = None
    level = None

    def __init__(self, userId = None):
        if userId is not None:
            self = db.get_user_with_id(userId)
        else:
            # empty constructor
            pass

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