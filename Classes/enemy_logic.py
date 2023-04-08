import db


class EnemyLogic:
    def __init__(self, idLogic):
        result = db.get_enemy_logic_with_id(idLogic)
        self.id = idLogic
        self.name = result[1]

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name
