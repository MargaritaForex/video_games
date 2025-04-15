from src.ecs.components.CPosition import CPosition
from src.ecs.components.CSurface import CSurface
from src.ecs.components.CHealth import CHealth
from src.ecs.components.CExplosion import CExplosion
from src.ecs.entities.factory import create_explosion

def system_collision(world):
    # Obtener todas las entidades con posición y superficie
    entities = []
    for entity_id, components in world.items():
        pos = components.get(CPosition)
        surface = components.get(CSurface)
        if pos and surface:
            entities.append((entity_id, pos, surface))
    
    # Verificar colisiones entre pares de entidades
    for i, (entity1_id, pos1, surface1) in enumerate(entities):
        for entity2_id, pos2, surface2 in entities[i+1:]:
            # Verificar colisión usando rectángulos
            rect1 = surface1.area.copy()
            rect1.x = pos1.x
            rect1.y = pos1.y
            
            rect2 = surface2.area.copy()
            rect2.x = pos2.x
            rect2.y = pos2.y
            
            if rect1.colliderect(rect2):
                # Reducir salud de ambas entidades
                health1 = world[entity1_id].get(CHealth)
                health2 = world[entity2_id].get(CHealth)
                
                if health1:
                    health1.current -= 1
                if health2:
                    health2.current -= 1
                
                # Crear explosión en el punto de colisión
                mid_x = (pos1.x + pos2.x) / 2
                mid_y = (pos1.y + pos2.y) / 2
                create_explosion(world, {"x": mid_x, "y": mid_y})
                
                # Eliminar entidades si su salud llega a 0
                if health1 and health1.current <= 0:
                    del world[entity1_id]
                if health2 and health2.current <= 0:
                    del world[entity2_id] 