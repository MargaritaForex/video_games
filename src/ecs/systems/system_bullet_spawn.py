import pygame
from src.ecs.components.CPosition import CPosition
from src.ecs.entities.factory import create_bullet

def system_bullet_spawn(world, mouse_pressed, player_entity, bullet_cfg):
    if mouse_pressed[0]:  # Click izquierdo
        pos = world.get_component(player_entity, CPosition)
        create_bullet(world, pos, bullet_cfg)
