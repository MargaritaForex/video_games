from src.ecs.components.CAnimation import CAnimation
from src.ecs.components.CExplosion import CExplosion

def system_explosion(world, delta_time: float):
    """Actualiza las explosiones y elimina las que ya han terminado su animación."""
    to_remove = []

    for entity_id, components in world.items():
        if CExplosion in components and CAnimation in components:
            animation = components[CAnimation]
            animation.update(delta_time)

            if animation.is_done():
                to_remove.append(entity_id)

    for entity_id in to_remove:
        del world[entity_id]
