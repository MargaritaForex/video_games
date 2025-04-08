# src/ecs/systems/system_movement.py
from src.ecs.components.CPosition import CPosition
from src.ecs.components.CVelocity import CVelocity
from src.ecs.components.CRect import CRect

def system_movement(entities, screen_w, screen_h, delta_time):
    for e in entities:
        pos = e.get(CPosition)
        vel = e.get(CVelocity)
        rect = e.get(CRect)
        if pos and vel and rect:
            pos.x += vel.vx * delta_time
            pos.y += vel.vy * delta_time

            # Rebote
            if pos.x <= 0 or pos.x + rect.w >= screen_w:
                vel.vx *= -1
            if pos.y <= 0 or pos.y + rect.h >= screen_h:
                vel.vy *= -1
