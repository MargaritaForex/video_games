from src.ecs.components.CEnemySpawner import CEnemySpawner
from src.create.prefab_creator import PrefabCreator

ENEMY_TYPE_MAPPING = {
    "enemy_a": "TypeA",
    "enemy_b": "TypeB",
    "enemy_c": "TypeC",
    "enemy_d": "TypeD",
    "hunter": "Hunter"
}

def system_enemy_spawner(engine, prefab_creator: PrefabCreator, delta_time):
    for entity_id in list(engine.entities.keys()):
        components = engine.entities[entity_id]
        spawner = components.get(CEnemySpawner)
        if not spawner:
            continue

        spawner.timer += delta_time

        for idx, spawn_event in enumerate(spawner.level_data):
            if idx in spawner.spawned:
                continue

            if spawner.timer >= spawn_event["time"]:
                raw_type = spawn_event["enemy_type"]
                mapped_type = ENEMY_TYPE_MAPPING.get(raw_type)

                if not mapped_type:
                    print(f"⚠ Tipo de enemigo desconocido: {raw_type}")
                    continue

                pos = spawn_event["position"]

                if mapped_type == "Hunter":
                    prefab_creator.create_hunter(pos)
                else:
                    prefab_creator.create_enemy(pos, mapped_type)

                spawner.spawned.add(idx)
