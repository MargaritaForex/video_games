import pygame
from src.ecs.components.CPosition import CPosition
from src.ecs.components.CSurface import CSurface
from src.ecs.components.CBullet import CBullet

def system_bullet_boundary(entities: dict, screen: pygame.Surface):
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    entities_to_remove = []

    for entity_id, components in entities.items():
        if CPosition in components and CSurface in components and CBullet in components:
            pos = components[CPosition]
            surf = components[CSurface]
            rect = surf.area.copy()
            rect.topleft = (pos.x, pos.y)

            if (
                rect.left < 0 or rect.right > screen_width or
                rect.top < 0 or rect.bottom > screen_height
            ):
                entities_to_remove.append(entity_id)

    for entity_id in entities_to_remove:
        del entities[entity_id]
        print(f"🚫 Bullet {entity_id} removed (out of bounds)")
