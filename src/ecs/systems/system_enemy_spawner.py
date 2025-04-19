# src/ecs/systems/system_enemy_spawner.py
from src.ecs.components.CEnemySpawner import CEnemySpawner
from src.create.prefab_creator import PrefabCreator


def system_enemy_spawner(engine, prefab_creator: PrefabCreator, delta_time):
    # Clonamos la lista de llaves (IDs de entidades)
    for entity_id in list(engine.entities.keys()):
        components = engine.entities[entity_id]
        spawner = components.get(CEnemySpawner)
        if spawner:
            spawner.timer += delta_time
            for idx, spawn_event in enumerate(spawner.level_data):
                if idx not in spawner.spawned and spawner.timer >= spawn_event["time"]:
                    enemy_type = spawn_event["enemy_type"]
                    pos = spawn_event["position"]

                    if enemy_type == "Hunter":
                        prefab_creator.create_hunter(pos)
                    else:
                        prefab_creator.create_enemy(pos, enemy_type)

                    spawner.spawned.add(idx)

