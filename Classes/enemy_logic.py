
class EnemyLogic:
    def __init__(self, idLogic):
        result = db.get_enemy_logic_with_id(idLogic)
        self.idLogic = result[0]
        self.name = result[1]



