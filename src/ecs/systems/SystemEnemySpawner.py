# src/ecs/systems/system_enemy_spawner.py
from src.ecs.components.CEnemySpawner import CEnemySpawner
from src.ecs.entities.factory import build_enemy_components

def system_enemy_spawner(engine, delta_time):
    for e in engine.entities:
        spawner = e.get(CEnemySpawner)
        if spawner:
            spawner.timer += delta_time
            for idx, spawn_event in enumerate(spawner.level_data):
                if idx not in spawner.spawned and spawner.timer >= spawn_event["time"]:
                    enemy_type = spawn_event["enemy_type"]
                    enemy_data = spawner.enemies_cfg[enemy_type]
                    enemy_entity = build_enemy_components(engine, spawn_event["position"], enemy_data)
                    spawner.spawned.add(idx)