# src/ecs/systems/system_movement.py
from src.ecs.components.CPosition import CPosition
from src.ecs.components.CVelocity import CVelocity
from src.ecs.components.CSurface import CSurface  # Asegúrate de importar esto

def system_movement(world, screen_width: int, screen_height: int, delta_time: float):
    for entity_id, components in world.items():
        pos = components.get(CPosition)
        vel = components.get(CVelocity)
        surface = components.get(CSurface)

        if pos and vel:
            pos.x += vel.vx * delta_time
            pos.y += vel.vy * delta_time

            if surface:
                width = surface.area.width
                height = surface.area.height
            else:
                width = 0
                height = 0

            # Limites más precisos (considerando el tamaño del sprite)
            if pos.x < 0:
                pos.x = 0
            elif pos.x > screen_width - width:
                pos.x = screen_width - width

            if pos.y < 0:
                pos.y = 0
            elif pos.y > screen_height - height:
                pos.y = screen_height - height