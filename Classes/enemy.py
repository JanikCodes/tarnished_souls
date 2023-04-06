
class Enemy:
    def __init__(self, idEnemy):
        result = db.get_enemy_with_id(idEnemy)
        self.id = idEnemy
        self.name = result[0]
        self.logic = EnemyLogic(result[1])
        self.description = result[2]
        self.health = result[3]
        self.runes = result[4]