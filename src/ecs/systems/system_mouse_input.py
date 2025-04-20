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
                # ⚠️ Creamos un nuevo diccionario con coordenadas ligeramente arriba del jugador
                bullet_spawn_pos = {
                    "x": position.x,
                    "y": position.y - 20  # más alto que antes
                }
                engine.prefab_creator.create_bullet(bullet_spawn_pos)
