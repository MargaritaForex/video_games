from src.ecs.components.CExplosion import CExplosion

def system_explosion(world, delta_time: float):
    for entity_id, components in world.items():
        explosion = components.get(CExplosion)
        if explosion:
            explosion.duration -= delta_time
            if explosion.duration <= 0:
                del world[entity_id] 