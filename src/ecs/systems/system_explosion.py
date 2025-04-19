# src/ecs/systems/system_explosion.py
from src.ecs.components.CAnimation import CAnimation
from src.ecs.components.CExplosion import CExplosion

def system_explosion(world, delta_time: float):
    entities_to_remove = []

    for entity_id, components in world.items():
        if CExplosion in components and CAnimation in components:
            anim = components[CAnimation]
            anim.update(delta_time)
            if anim.is_done():
                entities_to_remove.append(entity_id)

    for entity_id in entities_to_remove:
        del world[entity_id]

