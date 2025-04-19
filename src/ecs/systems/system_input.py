import pygame
from src.ecs.components.CVelocity import CVelocity

PLAYER_SPEED = 200

def system_input(engine):
    """Actualiza la velocidad del jugador en función de las teclas presionadas."""
    player_components = engine.entities.get(engine.player_entity)
    if not player_components:
        return

    velocity = player_components.get(CVelocity)
    if not velocity:
        return

    # Reiniciar velocidad a cero antes de aplicar dirección
    velocity.vx = 0
    velocity.vy = 0

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        velocity.vx = -PLAYER_SPEED
    elif keys[pygame.K_RIGHT]:
        velocity.vx = PLAYER_SPEED

    if keys[pygame.K_UP]:
        velocity.vy = -PLAYER_SPEED
    elif keys[pygame.K_DOWN]:
        velocity.vy = PLAYER_SPEED
