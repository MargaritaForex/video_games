# src/ecs/components/CEnemySpawner.py
class CEnemySpawner:
    def __init__(self, level_data: list):
        self.level_data = level_data  # Lista de eventos de enemigos
        self.timer = 0.0              # Acumulador de tiempo
        self.spawned = set()          # Índices ya spawneados
