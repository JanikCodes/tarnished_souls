import random


class EnemyMove:

    def __init__(self, idMove=None, description=None, phase=None, type=None, damage=None,\
                 healing=None, duration=None, max_targets=None):
        if idMove is not None:
            self.id = idMove
            self.description = description
            self.phase = phase
            self.type = type
            self.damage = damage
            self.healing = healing
            self.duration = duration
            self.max_targets = max_targets
        else:
            # empty constructor
            pass

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

    def set_id(self, move_id):
        self.id = move_id

    def set_description(self, description):
        self.description = description

    def set_phase(self, phase):
        self.phase = phase

    def set_type(self, type):
        self.type = type

    def set_damage(self, damage):
        self.damage = damage

    def set_healing(self, healing):
        self.healing = healing

    def set_duration(self, duration):
        self.duration = duration

    def set_max_targets(self, max_targets):
        self.max_targets = max_targets

    def overwrite_name_in_description(self, enemy_name):
        self.description = self.description.replace("@enemy", f"**{enemy_name}**")

    def execute(self, enemy, users):
        # TODO: Make a seperate move_type class and use those instead of the raw id's here

        match self.type:
            case 1:
                targets_list = [user for user in users if user.get_health() > 0]
                targets = random.sample(targets_list, min(self.max_targets, len(targets_list)))
                for target in targets:
                    if not target.get_is_dodging():
                        target.reduce_health(self.damage)

                    # Update user object
                    for i, user in enumerate(users):
                        if user == target:
                            users[i] = target
                            break
            case 2:
                # dodge
                enemy.dodge()
            case 3:
                # heal
                enemy.increase_health(self.healing)
                pass
            case 4:
                # block
                pass
            case 5:
                # leave blank
                pass

        return (enemy, users)
