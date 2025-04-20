from src.ecs.components.CPosition import CPosition
from src.ecs.components.CSurface import CSurface
from src.create.prefab_creator import PrefabCreator

def system_collision(world, prefab_creator: PrefabCreator):
    """Detecta colisiones y maneja explosiones y respawn del jugador."""
    entities = [(eid, comps.get(CPosition), comps.get(CSurface))
                for eid, comps in world.items() if comps.get(CPosition) and comps.get(CSurface)]

    def delete_and_respawn_if_player(entity_id):
        engine = prefab_creator._entity_manager
        if entity_id == engine.player_entity:
            del world[entity_id]
            player_cfg = prefab_creator.get_default_player_cfg()
            engine.player_entity = engine.prefab_creator.create_player(
                engine.player_spawn_position, {"vx": 0, "vy": 0}, player_cfg
            )
        else:
            del world[entity_id]

    for i, (eid1, pos1, surf1) in enumerate(entities):
        for eid2, pos2, surf2 in entities[i + 1:]:
            r1 = surf1.area.copy(); r1.topleft = (pos1.x, pos1.y)
            r2 = surf2.area.copy(); r2.topleft = (pos2.x, pos2.y)
            if r1.colliderect(r2):
                mx, my = (pos1.x + pos2.x) / 2, (pos1.y + pos2.y) / 2
                prefab_creator.create_explosion({"x": mx, "y": my})
                delete_and_respawn_if_player(eid1)
                delete_and_respawn_if_player(eid2)
