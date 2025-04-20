import pygame
from src.ecs.components.CSurface import CSurface
from src.ecs.components.CPosition import CPosition

def system_mouse_input(engine):
    mouse_pressed = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()

    if mouse_pressed[0]:  # Click izquierdo
        player_components = engine.entities.get(engine.player_entity)
        if not player_components:
            return

        surface = player_components.get(CSurface)
        position = player_components.get(CPosition)

        if surface and position:
            player_rect = surface.area.copy()
            player_rect.topleft = (position.x, position.y)
            if player_rect.collidepoint(mouse_pos):
                # Solo se dispara si se hace clic directamente sobre el jugador
                engine.prefab_creator.create_bullet(position)