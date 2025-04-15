import pygame
from src.ecs.components.CVelocity import CVelocity

def system_input(entities, player_entity, world):
    keys = pygame.key.get_pressed()
    vel = world.get_component(player_entity, CVelocity)
    
    # Reset velocity
    vel.vx = 0
    vel.vy = 0
    
    # Movement speed
    speed = 300
    
    # Handle movement
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        vel.vx = -speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        vel.vx = speed
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        vel.vy = -speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        vel.vy = speed 