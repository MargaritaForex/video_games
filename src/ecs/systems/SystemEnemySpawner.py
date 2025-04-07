# src/ecs/systems/system_enemy_spawner.py
from src.ecs.components.CEnemySpawner import CEnemySpawner
from src.ecs.entities.factory import create_enemy

def system_enemy_spawner(entities, delta_time):
    for e in entities:
        spawner = e.get(CEnemySpawner)
        if spawner:
            spawner.timer += delta_time

            for idx, enemy_data in enumerate(spawner.level_data):
                if idx not in spawner.spawned and spawner.timer >= enemy_data["spawn_time"]:
                    enemy_entity = create_enemy(enemy_data)
                    entities.append(enemy_entity)
                    spawner.spawned.add(idx)
