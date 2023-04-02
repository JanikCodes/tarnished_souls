import db

class Item:
    def __init__(self, idItem, name, iconCategory, item_type, reqVigor, reqMind, reqEndurance, reqStrength, reqDexterity, reqIntelligence, reqFaith, reqArcane, level, value, price, extra_value, obtainable, weight):
        self.idItem = idItem
        self.name = name
        self.iconCategory = iconCategory
        self.item_type = item_type
        self.reqVigor = reqVigor
        self.reqMind = reqMind
        self.reqEndurance = reqEndurance
        self.reqStrength = reqStrength
        self.reqDexterity = reqDexterity
        self.reqIntelligence = reqIntelligence
        self.reqFaith = reqFaith
        self.reqArcane = reqArcane
        self.level = level
        self.value = value
        self.price = price
        self.extra_value = extra_value
        self.obtainable = obtainable
        self.weight = weight

    # Getter methods
    def get_idItem(self):
        return self.idItem

    def get_name(self):
        return self.name

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

    def get_extra_value_text(self):
        if self.item_type == 'Weapon':
            return f"with **__{self.extra_value}__ bonus** damage! :star2:"
        else:
            return f"with **__{self.extra_value}__ bonus** armor! :star2:"