
class EnemyMove:

    def __init__(self, idMove, description, phase, type, damage, healing, duration, max_targets):
        self.id = idMove
        self.description = description
        self.phase = phase
        self.type = type
        self.damage = damage
        self.healing = healing
        self.duration = duration
        self.max_targets = max_targets

    def get_id(self):
        return self.id

    def get_description(self):
        return self.description

    def get_phase(self):
        return self.phase

    def get_type(self):
        return self.type

    def get_damage(self):
        return self.damage

    def get_healing(self):
        return self.healing

    def get_duration(self):
        return self.duration

    def get_max_targets(self):
        return self.max_targets