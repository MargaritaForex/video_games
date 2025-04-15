import pygame
from src.ecs.components.CVelocity import CVelocity
from src.ecs.constants import VELOCITY_X, VELOCITY_Y

def system_input(engine):
    # Obtener el jugador
    player_components = engine.entities.get(engine.player_entity)
    if not player_components:
        return
        
    # Obtener la velocidad del jugador
    velocity = player_components.get(CVelocity)
    if not velocity:
        return
        
    # Resetear velocidad
    velocity.vx = 0
    velocity.vy = 0
    
    # Obtener teclas presionadas
    keys = pygame.key.get_pressed()
    
    # Mover jugador
    if keys[pygame.K_LEFT]:
        velocity.vx = -200
    if keys[pygame.K_RIGHT]:
        velocity.vx = 200
    if keys[pygame.K_UP]:
        velocity.vy = -200
    if keys[pygame.K_DOWN]:
        velocity.vy = 200 