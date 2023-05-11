import db

SCALING_VALUES = {
    '-': 0,
    'E': 0.25,
    'D': 0.45,
    'C': 0.75,
    'B': 1.15,
    'A': 1.55,
    'S': 1.75,
}

WEAPON_DMG_INCREASE_PER_UPGRADE = 6

class Item:
    def __init__(self, idItem, name, iconCategory, item_type, reqVigor, reqMind, reqEndurance, reqStrength,
                 reqDexterity, reqIntelligence, reqFaith, reqArcane, price, obtainable, weight, value, iconUrl, sclVigor, sclMind, sclEndurance, sclStrength, sclDexterity, sclIntelligence, sclFaith, sclArcane):
        self.idItem = idItem
        self.name = name
        self.iconCategory = iconCategory
        self.item_type = item_type

        # Requirements
        self.reqVigor = reqVigor
        self.reqMind = reqMind
        self.reqEndurance = reqEndurance
        self.reqStrength = reqStrength
        self.reqDexterity = reqDexterity
        self.reqIntelligence = reqIntelligence
        self.reqFaith = reqFaith
        self.reqArcane = reqArcane

        #Scaling
        self.sclVigor = sclVigor
        self.sclMind = sclMind
        self.sclEndurance = sclEndurance
        self.sclStrength = sclStrength
        self.sclDexterity = sclDexterity
        self.sclIntelligence = sclIntelligence
        self.sclFaith = sclFaith
        self.sclArcane = sclArcane

        self.price = price
        self.value = value
        self.obtainable = obtainable
        self.weight = weight
        self.iconUrl = iconUrl

        self.level = 0
        self.extra_value = 0
        self.count = 1
        self.idRel = 0
        self.drop_rate = 100
        self.dropped_from_enemy_names = db.get_enemy_names_from_item_id(idItem=self.idItem)

    # Getter methods
    def get_icon_url(self):
        return self.iconUrl

    def get_idRel(self):
        return self.idRel

    def get_idItem(self):
        return self.idItem

    def get_name(self):
        return self.name

    def get_drop_rate(self):
        return self.drop_rate

    def get_scaling_value(self, scaling, attribute):
        val = 0
        if scaling != "-":
            val = SCALING_VALUES[scaling] * (self.value + self.extra_value) * (attribute / 100)
        return val

    def get_total_value(self, user):
        return self.get_value_with_scaling(user) + self.extra_value + self.get_level_value()

    def get_level_value(self):
        return self.level * WEAPON_DMG_INCREASE_PER_UPGRADE

    def get_value_with_scaling(self, user):
        return self.value + self.get_total_scaling_value(user)

    def get_total_scaling_value(self, user):
        total_value = 0
        total_value += self.get_scaling_value(self.sclVigor, user.get_vigor())
        total_value += self.get_scaling_value(self.sclMind, user.get_mind())
        total_value += self.get_scaling_value(self.sclEndurance, user.get_endurance())
        total_value += self.get_scaling_value(self.sclStrength, user.get_strength())
        total_value += self.get_scaling_value(self.sclDexterity, user.get_dexterity())
        total_value += self.get_scaling_value(self.sclIntelligence, user.get_intelligence())
        total_value += self.get_scaling_value(self.sclFaith, user.get_faith())
        total_value += self.get_scaling_value(self.sclArcane, user.get_arcane())
        return int(total_value)

    def get_iconCategory(self):
        return self.iconCategory

    def get_item_type(self):
        return self.item_type

    def get_reqVigor(self):
        return self.reqVigor

    def get_reqMind(self):
        return self.reqMind

    def get_reqEndurance(self):
        return self.reqEndurance

    def get_reqStrength(self):
        return self.reqStrength

    def get_reqDexterity(self):
        return self.reqDexterity

    def get_reqIntelligence(self):
        return self.reqIntelligence

    def get_reqFaith(self):
        return self.reqFaith

    def get_reqArcane(self):
        return self.reqArcane

    def get_level(self):
        return self.level

    def get_value(self):
        return self.value

    def get_price(self):
        return self.price

    def get_extra_value(self):
        return self.extra_value

    def get_obtainable(self):
        return self.obtainable

    def get_weight(self):
        return self.weight

    def get_count(self):
        return self.count

    def get_extra_value_text(self):
        if self.extra_value == 0:
            return str()
        elif self.item_type == 'Weapon':
            return f"with **__{self.extra_value}__ bonus** damage! :star2:"
        else:
            return f"with **__{self.extra_value}__ bonus** armor! :star2:"

    def set_level(self, level):
        self.dexterity = level

    def set_drop_rate(self, val):
        self.drop_rate = val

    def set_extra_value(self, extra_value):
        self.extra_value = extra_value

    def set_count(self, count):
        self.count = count

    def set_idRel(self, idRel):
        self.idRel = idRel

    def get_requirement_text(self):
        text = str()
        if self.reqVigor > 0:
            text += f"`Vig:` `{self.reqVigor}` "
        if self.reqMind > 0:
            text += f"`Min:` `{self.reqMind}` "
        if self.reqEndurance > 0:
            text += f"`End:` `{self.reqEndurance}` "
        if self.reqStrength > 0:
            text += f"`Str:` `{self.reqStrength}` "
        if self.reqDexterity > 0:
            text += f"`Dex:` `{self.reqDexterity}` "
        if self.reqIntelligence > 0:
            text += f"`Int:` `{self.reqIntelligence}` "
        if self.reqFaith > 0:
            text += f"`Fai:` `{self.reqFaith}` "
        if self.reqArcane > 0:
            text += f"`Arc:` `{self.reqArcane}` "

        if text == str():
            text = "`None`"

        return text

    def get_scaling_text(self):
        text = str()
        if self.sclVigor != "-":
            text += f"`Vig:` `{self.sclVigor}` "
        if self.sclMind != "-":
            text += f"`Min:` `{self.sclMind}` "
        if self.sclEndurance != "-":
            text += f"`End:` `{self.sclEndurance}` "
        if self.sclStrength != "-":
            text += f"`Str:` `{self.sclStrength}` "
        if self.sclDexterity != "-":
            text += f"`Dex:` `{self.sclDexterity}` "
        if self.sclIntelligence != "-":
            text += f"`Int:` `{self.sclIntelligence}` "
        if self.sclFaith != "-":
            text += f"`Fai:` `{self.sclFaith}` "
        if self.sclArcane != "-":
            text += f"`Arc:` `{self.sclArcane}` "

        if text == str():
            text = "`None`"

        return text

    def get_dropped_from_enemies_text(self):
        text = "from "
        for i, enemy_name in enumerate(self.dropped_from_enemy_names, start=1):
            if len(self.dropped_from_enemy_names) == i:
                text += f"`{enemy_name}`\n"
            else:
                text += f"`{enemy_name}` or "

        return text