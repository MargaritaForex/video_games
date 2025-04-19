import pygame
from src.ecs.components.CAnimation import CAnimation
from src.ecs.components.CSurface import CSurface


def system_animation(world, delta_time: float):
    for entity_id, components in world.items():
        animation = components.get(CAnimation)
        if animation:
            animation.update(delta_time)

            # Actualizar el área del sprite según el frame actual
            surface = components.get(CSurface)
            if surface:
                current_frame = animation.get_current_frame()
                full_width = surface.surface.get_width()
                height = surface.surface.get_height()

                frame_width = full_width // animation.num_frames
                surface.area = pygame.Rect(current_frame * frame_width, 0, frame_width, height)


