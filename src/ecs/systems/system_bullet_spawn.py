import pygame
import math
from src.ecs.components.CPosition import CPosition
from src.ecs.entities.factory import create_bullet

class BulletSpawner:
    def __init__(self):
        self.last_shot = 0
        self.shot_delay = 250  # milliseconds

def system_bullet_spawn(world, mouse_pressed, player_entity, bullet_cfg):
    current_time = pygame.time.get_ticks()
    
    if mouse_pressed[0] and current_time - world.bullet_spawner.last_shot > world.bullet_spawner.shot_delay:
        player_pos = world.get_component(player_entity, CPosition)
        mouse_pos = pygame.mouse.get_pos()
        
        # Calculate direction vector
        dx = mouse_pos[0] - player_pos.x
        dy = mouse_pos[1] - player_pos.y
        length = math.sqrt(dx * dx + dy * dy)
        
        if length > 0:
            # Normalize direction
            dx /= length
            dy /= length
            
            # Set bullet velocity
            bullet_cfg["velocity"]["x"] = dx * bullet_cfg["speed"]
            bullet_cfg["velocity"]["y"] = dy * bullet_cfg["speed"]
            
            create_bullet(world, player_pos, bullet_cfg)
            world.bullet_spawner.last_shot = current_time
