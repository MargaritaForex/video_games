# src/ecs/systems/system_enemy_spawner.py
from src.ecs.components.CEnemySpawner import CEnemySpawner
from src.ecs.entities.factory import create_enemy, create_hunter

def system_enemy_spawner(engine, delta_time):
    # Crear una copia del diccionario de entidades
    entities_copy = dict(engine.entities)
    
    for entity_id, components in entities_copy.items():
        spawner = components.get(CEnemySpawner)
        if spawner:
            spawner.timer += delta_time
            for idx, spawn_event in enumerate(spawner.level_data):
                if idx not in spawner.spawned and spawner.timer >= spawn_event["time"]:
                    enemy_type = spawn_event["enemy_type"]
                    enemy_data = spawner.enemies_cfg[enemy_type]
                    pos = spawn_event["position"]
                    
                    # Crear el enemigo
                    if enemy_type == "Hunter":
                        enemy_entity = create_hunter(engine, pos, enemy_data)
                    else:
                        enemy_entity = create_enemy(engine, pos, enemy_data)
                    
                    spawner.spawned.add(idx)
