# src/ecs/systems/system_movement.py
from src.ecs.components.CPosition import CPosition
from src.ecs.components.CVelocity import CVelocity
from src.ecs.components.CSurface import CSurface  # 🔹 importa el componente

def system_movement(world, screen_width: int, screen_height: int, delta_time: float):
    for entity_id, components in world.items():
        pos = components.get(CPosition)
        vel = components.get(CVelocity)
        surface = components.get(CSurface)  # 🔹 obtenemos el componente de superficie

        if pos and vel:
            pos.x += vel.vx * delta_time
            pos.y += vel.vy * delta_time

            # Si tenemos el componente surface, usamos sus dimensiones
            if surface:
                sprite_width = surface.surface.get_width()
                sprite_height = surface.surface.get_height()
            else:
                sprite_width = 0
                sprite_height = 0

            # 🔒 Limitar dentro de los bordes visibles de la pantalla
            if pos.x < 0:
                pos.x = 0
            elif pos.x > screen_width - sprite_width:
                pos.x = screen_width - sprite_width

            if pos.y < 0:
                pos.y = 0
            elif pos.y > screen_height - sprite_height:
                pos.y = screen_height - sprite_height
