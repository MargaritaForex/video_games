from src.ecs.components.CAnimation import CAnimation

def system_explosion(world, delta_time: float):
    to_remove = []
    for entity_id, components in world.items():
        if CAnimation in components:
            anim = components[CAnimation]
            anim.update(delta_time)
            if anim.is_done():
                to_remove.append(entity_id)

    # Eliminar explosiones que ya terminaron
    for entity_id in to_remove:
        del world[entity_id]
