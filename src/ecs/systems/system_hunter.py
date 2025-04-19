import math
from src.ecs.components.CPosition import CPosition
from src.ecs.components.CVelocity import CVelocity
from src.ecs.components.CHunter import CHunter
from src.ecs.components.CAnimation import CAnimation

def system_hunter(world, player_entity, delta_time: float):
    if player_entity not in world:
        return
    player_pos = world[player_entity].get(CPosition)
    if not player_pos:
        return
        
    for entity_id, components in world.items():
        hunter = components.get(CHunter)
        if not hunter:
            continue
            
        pos = components.get(CPosition)
        vel = components.get(CVelocity)
        if not pos or not vel:
            continue
            
        # Calcular distancia al jugador
        dx = player_pos.x - pos.x
        dy = player_pos.y - pos.y
        distance = (dx**2 + dy**2)**0.5
        
        # Comportamiento del cazador
        if distance < hunter.chase_distance:
            # Perseguir al jugador
            vel.vx = (dx / distance) * hunter.chase_speed
            vel.vy = (dy / distance) * hunter.chase_speed
        elif distance > hunter.return_distance:
            # Regresar a la posición inicial
            vel.vx = -vel.vx
            vel.vy = -vel.vy
        
        # Actualizar animación
        anim = components.get(CAnimation)
        if anim:
            if distance < hunter.chase_distance or distance > hunter.return_distance:
                anim.set_animation("MOVE")
            else:
                anim.set_animation("IDLE") 