from src.ecs.components.CPosition import CPosition
from src.ecs.components.CSurface import CSurface
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
                mid_x = (pos1.x + pos2.x) / 2
                mid_y = (pos1.y + pos2.y) / 2
                prefab_creator.create_explosion({"x": mid_x, "y": mid_y})

                engine = prefab_creator._entity_manager

                # Eliminar jugador y respawn
                def delete_and_respawn_if_player(entity_id):
                    if entity_id == engine.player_entity:
                        del world[entity_id]
                        player_cfg = {
                            "image": "assets/img/player.png",
                            "animation": {
                                "total_frames": 4,
                                "frame_rate": 10
                            }
                        }
                        engine.player_entity = engine.prefab_creator.create_player(
                            engine.player_spawn_position,
                            {"vx": 0, "vy": 0},
                            player_cfg
                        )
                    else:
                        del world[entity_id]

                delete_and_respawn_if_player(entity1_id)
                delete_and_respawn_if_player(entity2_id)
