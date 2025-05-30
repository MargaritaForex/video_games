# src/ecs/systems/system_render.py
from src.ecs.components.CPosition import CPosition
from src.ecs.components.CSurface import CSurface


def system_render(world, screen):
    """Dibuja todas las entidades que tengan posición y superficie en pantalla."""
    for _, components in world.items():
        pos = components.get(CPosition)
        surface = components.get(CSurface)

        if pos and surface:
            screen.blit(surface.surface, (pos.x, pos.y), surface.area)


