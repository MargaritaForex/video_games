# src/ecs/components/CEnemySpawner.py
class CEnemySpawner:
    def __init__(self, level_data, enemies_cfg):
        self.level_data = level_data  # Lista de eventos de spawn
        self.enemies_cfg = enemies_cfg  # Configuración de enemigos
        self.timer = 0.0  # Tiempo acumulado
        self.spawned = set()  # Índices de eventos ya ejecutados