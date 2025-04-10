# src/ecs/entities/factory.py
from src.ecs.components.CBullet import CBullet
from src.ecs.components.CPosition import CPosition
from src.ecs.components.CVelocity import CVelocity
from src.ecs.components.CRect import CRect
from src.ecs.components.CColor import CColor
from src.ecs.components.CEnemySpawner import CEnemySpawner
import random


def create_enemy(enemy_data):
    x = enemy_data.get("x", 0)
    y = enemy_data.get("y", 0)
    return {
        CPosition: CPosition(x, y),
        CVelocity: CVelocity(enemy_data["speed"]["x"], enemy_data["speed"]["y"]),
        CRect: CRect(enemy_data["size"]["w"], enemy_data["size"]["h"]),
        CColor: CColor(enemy_data["color"]["r"], enemy_data["color"]["g"], enemy_data["color"]["b"])
    }

def create_enemy_components(enemy_events, enemy_types_data):
    return {
        CEnemySpawner: CEnemySpawner(enemy_events, enemy_types_data)
    }


def build_enemy_components(engine, position, enemy_cfg):
    enemy = engine.create_entity()

    size = enemy_cfg["size"]
    color = enemy_cfg["color"]
    velocity = random.randint(enemy_cfg["velocity_min"], enemy_cfg["velocity_max"])

    engine.add_component(enemy, CPosition(position["x"], position["y"]))
    engine.add_component(enemy, CColor(color["r"], color["g"], color["b"]))
    engine.add_component(enemy, CVelocity(0, velocity))
    engine.add_component(enemy, CRect(size["x"], size["y"]))

    return enemy

def create_player(world, pos, vel, size, color):
    entity = world.create_entity()
    world.add_component(entity, CPosition(pos["x"], pos["y"]))  # Diccionario {"x": ..., "y": ...}
    world.add_component(entity, CVelocity(vel["x"], vel["y"]))
    world.add_component(entity, CRect(size["x"], size["y"]))
    world.add_component(entity, CColor(color["r"], color["g"], color["b"]))
    return entity


def create_bullet(world, pos: CPosition, cfg: dict):
    bullet = world.create_entity()
    world.add_component(bullet, CPosition(pos.x, pos.y))
    world.add_component(bullet, CVelocity(0, -cfg["velocity"]))  # hacia arriba
    world.add_component(bullet, CColor(cfg["color"]["r"], cfg["color"]["g"], cfg["color"]["b"]))
    world.add_component(bullet, CRect(cfg["size"]["x"], cfg["size"]["y"]))
    world.add_component(bullet, CBullet())  # puedes ajustar si quieres daño
    return bullet