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
                # Crear una explosión visual en el punto medio de la colisión
                mid_x = (pos1.x + pos2.x) / 2
                mid_y = (pos1.y + pos2.y) / 2
                prefab_creator.create_explosion({"x": mid_x, "y": mid_y})

                # Eliminar las dos entidades al colisionar
                if entity1_id in world:
                    del world[entity1_id]
                if entity2_id in world:
                    del world[entity2_id]
