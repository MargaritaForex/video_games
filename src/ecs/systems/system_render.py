# src/ecs/systems/system_render.py
import pygame
from src.ecs.components.CTransform import CTransform
from src.ecs.components.CSurface import CSurface


def system_render(world, screen):
    for entity_id, components in world.items():
        transform = components.get(CTransform)
        surface = components.get(CSurface)

        if transform and surface:
            screen.blit(surface.surface, (transform.pos.x, transform.pos.y))

