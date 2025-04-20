from src.ecs.components.CEnemySpawner import CEnemySpawner
from src.create.prefab_creator import PrefabCreator

def system_enemy_spawner(engine, prefab_creator: PrefabCreator, delta_time):
    """Genera enemigos según los eventos definidos en el nivel."""
    for entity_id, components in list(engine.entities.items()):
        spawner = components.get(CEnemySpawner)
        if not spawner:
            continue

        spawner.timer += delta_time
        for idx, spawn_event in enumerate(spawner.level_data):
            if idx in spawner.spawned or spawner.timer < spawn_event["time"]:
                continue

            pos = spawn_event["position"]
            if spawn_event["enemy_type"] == "Hunter":
                prefab_creator.create_hunter(pos)
            else:
                prefab_creator.create_enemy(pos, spawn_event["enemy_type"])

            spawner.spawned.add(idx)