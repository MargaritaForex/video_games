import pygame
from src.ecs.components.CAnimation import CAnimation
from src.ecs.components.CSurface import CSurface

def system_animation(world, delta_time: float):
    """Actualiza el cuadro actual de las entidades animadas."""
    for _, comps in world.items():
        anim = comps.get(CAnimation)
        surface = comps.get(CSurface)
        if anim and surface:
            anim.update(delta_time)
            frame = anim.get_current_frame()
            width = surface.surface.get_width() // anim.num_frames
            height = surface.surface.get_height()
            surface.area = pygame.Rect(frame * width, 0, width, height)



