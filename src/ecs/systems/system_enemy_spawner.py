# src/ecs/systems/system_enemy_spawner.py
from src.ecs.entities.factory import create_enemy

def system_enemy_spawner(level_data, entities, timer, spawned):
    for idx, enemy_data in enumerate(level_data):
        if idx not in spawned and timer >= enemy_data["spawn_time"]:
            e = create_enemy(enemy_data)
            entities.append(e)
            spawned.add(idx)
