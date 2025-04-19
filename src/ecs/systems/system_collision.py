from src.ecs.components.CPosition import CPosition
from src.ecs.components.CSurface import CSurface
from src.ecs.components.CHealth import CHealth
from src.create.prefab_creator import PrefabCreator

def system_collision(world, prefab_creator: PrefabCreator):
    entities = []
    for entity_id, components in world.items():
        pos = components.get(CPosition)
        surface = components.get(CSurface)
        if pos and surface:
            entities.append((entity_id, pos, surface))

    for i, (entity1_id, pos1, surface1) in enumerate(entities):
        for entity2_id, pos2, surface2 in entities[i + 1:]:
            rect1 = surface1.area.copy()
            rect1.x = pos1.x
            rect1.y = pos1.y

            rect2 = surface2.area.copy()
            rect2.x = pos2.x
            rect2.y = pos2.y

            if rect1.colliderect(rect2):
                health1 = world[entity1_id].get(CHealth)
                health2 = world[entity2_id].get(CHealth)

                if health1:
                    health1.current -= 1
                if health2:
                    health2.current -= 1

                mid_x = (pos1.x + pos2.x) / 2
                mid_y = (pos1.y + pos2.y) / 2
                prefab_creator.create_explosion({"x": mid_x, "y": mid_y})

                # 🟢 NUEVO: respawn si el jugador muere
                engine = prefab_creator._entity_manager
                if health1 and health1.current <= 0:
                    if entity1_id == engine.player_entity:
                        del world[entity1_id]
                        engine.player_entity = engine.prefab_creator.create_player(
                            engine.player_spawn_position,
                            { "vx": 0, "vy": 0 },
                            engine.bullet_cfg  # o player_cfg si tienes acceso
                        )
                    else:
                        del world[entity1_id]

                if health2 and health2.current <= 0:
                    if entity2_id == engine.player_entity:
                        del world[entity2_id]
                        engine.player_entity = engine.prefab_creator.create_player(
                            engine.player_spawn_position,
                            { "vx": 0, "vy": 0 },
                            engine.bullet_cfg  # o player_cfg si tienes acceso
                        )
                    else:
                        del world[entity2_id]
