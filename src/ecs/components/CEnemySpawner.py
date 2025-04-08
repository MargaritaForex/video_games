# src/ecs/components/CEnemySpawner.py
class CEnemySpawner:
    def __init__(self, level_data, enemies_cfg):
        self.level_data = level_data
        self.enemies_cfg = enemies_cfg
        self.timer = 0.0
        self.spawned = set()