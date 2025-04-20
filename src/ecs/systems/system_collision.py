from src.ecs.components.CPosition import CPosition
from src.ecs.components.CSurface import CSurface
from src.create.prefab_creator import PrefabCreator

def system_collision(world, prefab_creator: PrefabCreator):
    """Detecta colisiones, genera explosiones y respawnea al jugador si colisiona."""

    engine = prefab_creator._entity_manager

    # Extrae entidades con posición y superficie
    entities = [
        (eid, comps[CPosition], comps[CSurface])
        for eid, comps in world.items()
        if CPosition in comps and CSurface in comps
    ]

    def handle_entity_removal(entity_id):
        if entity_id == engine.player_entity:
            del world[entity_id]
            player_cfg = prefab_creator.get_default_player_cfg()
            engine.player_entity = engine.prefab_creator.create_player(
                engine.player_spawn_position,
                {"vx": 0, "vy": 0},
                player_cfg
            )
        else:
            del world[entity_id]

    # Detecta colisiones por pares
    for i, (eid1, pos1, surf1) in enumerate(entities):
        for eid2, pos2, surf2 in entities[i + 1:]:
            rect1 = surf1.area.copy(); rect1.topleft = (pos1.x, pos1.y)
            rect2 = surf2.area.copy(); rect2.topleft = (pos2.x, pos2.y)

            if rect1.colliderect(rect2):
                mid_x = (pos1.x + pos2.x) / 2
                mid_y = (pos1.y + pos2.y) / 2
                prefab_creator.create_explosion({"x": mid_x, "y": mid_y})

                handle_entity_removal(eid1)
                handle_entity_removal(eid2)
