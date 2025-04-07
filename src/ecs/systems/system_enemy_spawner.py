# src/ecs/systems/system_enemy_spawner.py
from src.ecs.components.CEnemySpawner import CEnemySpawner
from src.ecs.entities.factory import create_enemy

def system_enemy_spawner(engine, delta_time):
    entities = engine.get_entities_with_components(CEnemySpawner)
    for e in entities:
        spawner = engine.get_component(e, CEnemySpawner)
        spawner.timer += delta_time

        for idx, enemy_data in enumerate(spawner.level_data):
            if idx not in spawner.spawned and spawner.timer >= enemy_data["spawn_time"]:
                enemy_e = engine.create_entity()
                components = create_enemy(enemy_data)
                for c_type, component in components.items():
                    engine.add_component(enemy_e, component)
                spawner.spawned.add(idx)

                # 🔍 Print de depuración detallado
                print(f"[Spawner] Enemigo {idx} creado: posición ({enemy_data['x']}, {enemy_data['y']}), "
                      f"velocidad ({enemy_data['speed']['x']}, {enemy_data['speed']['y']}), "
                      f"tiempo de aparición: {enemy_data['spawn_time']}s")
