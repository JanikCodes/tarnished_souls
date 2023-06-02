import db

WEAPON_DMG_INCREASE_PER_UPGRADE = 6


class Item:
    def __init__(self, idItem):
        filled_item = db.get_item_from_item_id(idItem=idItem)
        self.idItem = filled_item[0]
        self.name = filled_item[1]
        self.iconCategory = filled_item[2]
        self.item_type = filled_item[3]

        # Requirements
        self.reqVigor = filled_item[4]
        self.reqMind = filled_item[5]
        self.reqEndurance = filled_item[6]
        self.reqStrength = filled_item[7]
        self.reqDexterity = filled_item[8]
        self.reqIntelligence = filled_item[9]
        self.reqFaith = filled_item[10]
        self.reqArcane = filled_item[11]

        # Scaling
        self.sclVigor = filled_item[17]
        self.sclMind = filled_item[18]
        self.sclEndurance = filled_item[19]
        self.sclStrength = filled_item[20]
        self.sclDexterity = filled_item[21]
        self.sclIntelligence = filled_item[22]
        self.sclFaith = filled_item[23]
        self.sclArcane = filled_item[24]

        self.price = filled_item[13]
        self.value = filled_item[12]
        self.obtainable = filled_item[14]
        self.weight = filled_item[15]
        self.iconUrl = filled_item[16]

        self.level = 0
        self.extra_value = 0
        self.count = 1
        self.idRel = 0
        self.favorite = 0
        self.drop_rate = 100
        self.dropped_from_enemy_names = db.get_enemy_names_from_item_id(idItem=self.idItem)

    # Getter methods
    def get_icon_url(self):
        return self.iconUrl

    def get_idRel(self):
        return self.idRel

    def get_favorite(self):
        return self.favorite

    def get_idItem(self):
        return self.idItem

    def get_name(self):
        return self.name

    def get_drop_rate(self):
        return self.drop_rate

    def get_scaling_value(self, scaling, attribute):
        val = 0
        if scaling != "-":
            val = self.get_total_scaling_value_(scaling) * (self.value + self.extra_value) * (attribute / 100) + (
                        self.level * 1.05)
        return val

    def get_total_value(self, user):
        return self.get_value_with_scaling(user) + self.extra_value

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
        self.level = level

    def set_favorite(self, favorite):
        self.favorite = favorite

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

    def get_scaling_character_from_value(self, value):
        if value > 1.75:
            return "S"
        elif value >= 1.4:
            return "A"
        elif value >= 0.9:
            return "B"
        elif value >= 0.6:
            return "C"
        elif value >= 0.25:
            return "D"
        else:
            return "E"

    def get_total_scaling_value_(self, value):
        return (value / 100) + (self.level * (value / 100) * 0.02)

    def get_scaling_text(self):
        text = str()
        if self.sclVigor != 0:
            text += f"`Vig:` `{self.get_scaling_character_from_value(self.get_total_scaling_value_(self.sclVigor))}` "
        if self.sclMind != 0:
            text += f"`Min:` `{self.get_scaling_character_from_value(self.get_total_scaling_value_(self.sclMind))}` "
        if self.sclEndurance != 0:
            text += f"`End:` `{self.get_scaling_character_from_value(self.get_total_scaling_value_(self.sclEndurance))}` "
        if self.sclStrength != 0:
            text += f"`Str:` `{self.get_scaling_character_from_value(self.get_total_scaling_value_(self.sclStrength))}` "
        if self.sclDexterity != 0:
            text += f"`Dex:` `{self.get_scaling_character_from_value(self.get_total_scaling_value_(self.sclDexterity))}` "
        if self.sclIntelligence != 0:
            text += f"`Int:` `{self.get_scaling_character_from_value(self.get_total_scaling_value_(self.sclIntelligence))}` "
        if self.sclFaith != 0:
            text += f"`Fai:` `{self.get_scaling_character_from_value(self.get_total_scaling_value_(self.sclFaith))}` "
        if self.sclArcane != 0:
            text += f"`Arc:` `{self.get_scaling_character_from_value(self.get_total_scaling_value_(self.sclArcane))}` "

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
