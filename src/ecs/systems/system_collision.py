from src.ecs.components.CTransform import CTransform
from src.ecs.components.CSurface import CSurface
from src.ecs.components.CHealth import CHealth
from src.create.prefab_creator import PrefabCreator

def system_collision(world, prefab_creator: PrefabCreator):
    # Obtener todas las entidades con transform y superficie
    entities = []
    for entity_id, components in world.items():
        transform = components.get(CTransform)
        surface = components.get(CSurface)
        if transform and surface:
            entities.append((entity_id, transform, surface))
    
    # Verificar colisiones entre pares de entidades
    for i, (entity1_id, transform1, surface1) in enumerate(entities):
        for entity2_id, transform2, surface2 in entities[i+1:]:
            # Verificar colisión usando rectángulos
            rect1 = surface1.area.copy()
            rect1.x = transform1.pos.x
            rect1.y = transform1.pos.y
            
            rect2 = surface2.area.copy()
            rect2.x = transform2.pos.x
            rect2.y = transform2.pos.y
            
            if rect1.colliderect(rect2):
                # Reducir salud de ambas entidades
                health1 = world[entity1_id].get(CHealth)
                health2 = world[entity2_id].get(CHealth)
                
                if health1:
                    health1.current -= 1
                if health2:
                    health2.current -= 1
                
                # Crear explosión en el punto de colisión
                mid_x = (transform1.pos.x + transform2.pos.x) / 2
                mid_y = (transform1.pos.y + transform2.pos.y) / 2
                prefab_creator.create_explosion({"x": mid_x, "y": mid_y})
                
                # Eliminar entidades si su salud llega a 0
                if health1 and health1.current <= 0:
                    del world[entity1_id]
                if health2 and health2.current <= 0:
                    del world[entity2_id] 