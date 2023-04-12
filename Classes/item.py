
SCALING_VALUES = {
    '-': 0,
    'E': 0.25,
    'D': 0.45,
    'C': 0.75,
    'B': 1.15,
    'A': 1.55,
    'S': 1.75,
}

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
        self.count = 0
        self.idRel = 0

    # Getter methods
    def get_icon_url(self):
        return self.iconUrl

    def get_idRel(self):
        return self.idRel

    def get_idItem(self):
        return self.idItem

    def get_name(self):
        return self.name

    def get_scaling_value(self, scaling, attribute):
        val = 0
        if scaling != "-":
            val = SCALING_VALUES[scaling] * (self.value + self.extra_value) * (attribute / 100)
        return val

    def get_total_value(self, user):
        return self.value + self.extra_value + self.get_total_scaling_value(user)

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

    def set_extra_value(self, extra_value):
        self.extra_value = extra_value

    def set_count(self, count):
        self.count = count

    def set_idRel(self, idRel):
        self.idRel = idRel

    def get_requirement_text(self):
        text = str()
        text += f"`Vig:` `{self.reqVigor}` "
        text += f"`Str:` `{self.reqMind}` "
        text += f"`End:` `{self.reqEndurance}` "
        text += f"`Str:` `{self.reqStrength}` "
        text += f"`Dex:` `{self.reqDexterity}` "
        text += f"`Int:` `{self.reqIntelligence}` "
        text += f"`Fai:` `{self.reqFaith}` "

        return text

    def get_scaling_text(self):
        text = str()
        text += f"`Vig:` `{self.sclVigor}` "
        text += f"`Min:` `{self.sclMind}` "
        text += f"`End:` `{self.sclEndurance}` "
        text += f"`Str:` `{self.sclStrength}` "
        text += f"`Dex:` `{self.sclDexterity}` "
        text += f"`Int:` `{self.sclIntelligence}` "
        text += f"`Fai:` `{self.sclFaith}` "

        return text