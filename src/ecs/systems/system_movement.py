# src/ecs/systems/system_movement.py

from src.ecs.components.CPosition import CPosition
from src.ecs.components.CVelocity import CVelocity
from src.ecs.components.CSurface import CSurface

def system_movement(world, screen_width: int, screen_height: int, delta_time: float):
    """Actualiza la posición de las entidades con velocidad y aplica límites de pantalla."""
    for _, components in world.items():
        pos = components.get(CPosition)
        vel = components.get(CVelocity)

        if not pos or not vel:
            continue

        pos.x += vel.vx * delta_time
        pos.y += vel.vy * delta_time

        surface = components.get(CSurface)
        width = surface.area.width if surface else 0
        height = surface.area.height if surface else 0

        clamp_position(pos, width, height, screen_width, screen_height)

def clamp_position(pos, width, height, screen_width, screen_height):
    """Restringe la posición dentro de los límites de la pantalla."""
    pos.x = max(0, min(pos.x, screen_width - width))
    pos.y = max(0, min(pos.y, screen_height - height))
