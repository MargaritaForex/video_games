import random
from src.ecs.components.CEnemy import CEnemy

class SystemEnemySpawner:
    def __init__(self, level_data, entities):
        """Inicializa el sistema de spawn de enemigos."""
        if isinstance(level_data, dict):
            self.level_data = level_data.get("enemies", [])  # Asegurar que sea lista
        elif isinstance(level_data, list):
            self.level_data = level_data  # Ya es lista
        else:
            print("❌ Error: level_data tiene un formato incorrecto", type(level_data))
            self.level_data = []

        self.entities = entities
        self.timer = 0  # 📌 Se agrega el temporizador inicial

    def update(self, delta_time):
        """Genera enemigos según el tiempo definido en level_01.json"""
        self.timer += delta_time  # 📌 Ahora usa self.timer correctamente

        for enemy_data in self.level_data:
            spawn_time = enemy_data.get("spawn_time", 0)

            if self.timer >= spawn_time:
                new_enemy = CEnemy(
                    x=random.randint(50, 590),
                    y=random.randint(50, 310),
                    w=enemy_data["size"]["w"],
                    h=enemy_data["size"]["h"],
                    speed_x=enemy_data["speed"]["x"],
                    speed_y=enemy_data["speed"]["y"],
                    color=(
                        enemy_data["color"]["r"],
                        enemy_data["color"]["g"],
                        enemy_data["color"]["b"],
                    )
                )
                self.entities.append(new_enemy)
                self.timer = 0  # 📌 Reinicia el temporizador después del spawn
