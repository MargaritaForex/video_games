# src/ecs/systems/system_movement.py
from src.ecs.components.CPosition import CPosition
from src.ecs.components.CVelocity import CVelocity

def system_movement(world, screen_width: int, screen_height: int, delta_time: float):
    for entity_id, components in world.items():
        pos = components.get(CPosition)
        vel = components.get(CVelocity)
        
        if pos and vel:
            pos.x += vel.vx * delta_time
            pos.y += vel.vy * delta_time
            
            # Mantener la entidad dentro de los límites de la pantalla
            if pos.x < 0:
                pos.x = 0
            elif pos.x > screen_width:
                pos.x = screen_width
                
            if pos.y < 0:
                pos.y = 0
            elif pos.y > screen_height:
                pos.y = screen_height
