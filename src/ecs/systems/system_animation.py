import pygame
from src.ecs.components.CAnimation import CAnimation
from src.ecs.components.CSurface import CSurface


def system_animation(world, delta_time: float):
    for entity_id, components in world.items():
        animation = components.get(CAnimation)
        if animation:
            animation.update(delta_time)

            surface = components.get(CSurface)
            if surface:
                current_frame = animation.get_current_frame()
                frame_width = surface.surface.get_width() // animation.num_frames
                frame_height = surface.surface.get_height()

                surface.area = pygame.Rect(
                    current_frame * frame_width, 0, frame_width, frame_height
                )

