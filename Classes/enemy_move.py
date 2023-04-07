import random


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

    def execute(self, enemy, users):
        #TODO: Make a seperate move_type class and use those instead of the raw id's here

        match self.type:
            case 1:
                targets_list = [user for user in users if user.get_health() > 0]
                targets = random.sample(targets_list, min(self.max_targets, len(targets_list)))
                for target in targets:
                    target.reduce_health(self.damage)
                    # Update user object
                    for i, user in enumerate(users):
                        if user == target:
                            users[i] = target
                            break
            case 2:
                pass
            case 3:
                enemy.increase_health(self.healing)
                pass
            case 4:
                pass
            case 5:
                pass


        return (enemy, users)
