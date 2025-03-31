import random
from src.ecs.components.CEnemy import CEnemy

class SystemEnemySpawner:
    def __init__(self, level_data, entities):
        """Inicializa el sistema de spawn de enemigos."""
        self.level_data = level_data  # Ya es una lista de enemigos
        self.entities = entities
        self.timer = 0
        self.spawned_enemies = set()  # 📌 Mantener un registro de enemigos creados

    def update(self, delta_time):
        """Genera enemigos según el tiempo definido en level_01.json"""
        self.timer += delta_time  # ✅ Usa self.timer correctamente

        for index, enemy_data in enumerate(self.level_data):
            spawn_time = enemy_data.get("spawn_time", 0)

            # 📌 Solo crear enemigos que no han sido generados antes
            if self.timer >= spawn_time and index not in self.spawned_enemies:
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
                self.spawned_enemies.add(index)  # 📌 Marcar enemigo como genera
