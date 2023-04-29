import random

import db
from Classes.enemy_logic import EnemyLogic


class Enemy:
    def __init__(self, idEnemy):
        result = db.get_enemy_with_id(idEnemy)
        self.id = idEnemy
        self.name = result[0]
        self.logic = EnemyLogic(result[1])
        self.description = result[2]
        self.max_health = result[3]
        self.runes = result[4]
        self.moves = db.get_enemy_moves_with_enemy_id(idEnemy)
        self.location = db.get_location_from_id(result[5])
        self.item_rewards = db.get_items_from_enemy_id(idEnemy=idEnemy)

        self.health = self.get_max_health()
        self.phase = 0
        self.last_move = None
        self.dodge_next = False
        self.last_move_text = str()

    def get_id(self):
        return self.id

    def get_last_move_text(self):
        return self.last_move_text

    def get_name(self):
        return self.name

    def get_logic(self):
        return self.logic

    def get_description(self):
        return self.description

    def get_health(self):
        return self.health

    def get_runes(self):
        return self.runes

    def get_max_health(self):
        return self.max_health

    def get_phase(self):
        return self.phase

    def reduce_health(self, amount):
        self.health = max(self.health - amount, 0)
        self.last_move_text = f"`-{amount}`"

    def increase_health(self, amount):
        self.health = min(self.health + amount, self.max_health)
        self.last_move_text = f"`+{amount}`"

    def set_health(self, amount):
        self.health = amount

    def get_move(self, phase):
        available_moves = [move for move in self.moves if
                           move != self.last_move and (move.get_phase() == phase or move.get_phase() == 0)]
        if available_moves:
            selected_move = random.choice(available_moves)
            self.last_move = selected_move
            return selected_move
        else:
            print("Didn't found a valid move anymore!")
            return None

    def dodge(self):
        self.dodge_next = True

    def get_is_dodging(self):
        if self.dodge_next:
            self.last_move_text = f"`dodged!`"
        return self.dodge_next

    def clear_last_move_text(self):
        self.last_move_text = str()

    def reset_dodge(self):
        self.dodge_next = False

    def increase_phase(self):
        self.phase += 1

    def set_max_health(self, health):
        self.max_health = health
        self.health = health

    def get_location(self):
        return self.location

    def get_item_rewards(self):
        items = []
        for item in self.item_rewards:
            rand = random.randint(0, 100)

            if item.get_drop_rate() >= rand:
                # we drop it.
                items.append(item)

        return items
