import db

BASE_HEALTH = 300
BASE_DAMAGE = 25
BASE_STAMINA = 100

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
            self.weapon = db.get_item_from_user_with_id_rel(idUser=userId, idRel=result[14])
            self.head = db.get_item_from_user_with_id_rel(idUser=userId, idRel=result[15])
            self.chest = db.get_item_from_user_with_id_rel(idUser=userId, idRel=result[16])
            self.legs = db.get_item_from_user_with_id_rel(idUser=userId, idRel=result[17])
            self.gauntlet = db.get_item_from_user_with_id_rel(idUser=userId, idRel=result[18])

            self.health = self.get_max_health()
            self.stamina = self.get_max_stamina()
            self.remaining_flasks = 0
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

    def get_weapon(self):
        return self.weapon

    def get_head(self):
        return self.head

    def get_chest(self):
        return self.chest

    def get_legs(self):
        return self.legs

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
        return BASE_HEALTH + (self.vigor * 2)
        #TODO Make better calculation ( maybe real one from wiki )

    def reduce_health(self, amount):
        self.health = max(self.health - amount, 0)

    def increase_health(self, amount):
        self.health = min(self.health + amount, self.get_max_health())

    def get_damage(self):
        if self.weapon is not None:
            return BASE_DAMAGE + self.weapon.get_total_value()
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
        return max(BASE_STAMINA - self.get_total_weight(), 0)

    def get_stamina(self):
        return self.stamina