# src/ecs/entities/factory.py
from src.ecs.components.CPosition import CPosition
from src.ecs.components.CVelocity import CVelocity
from src.ecs.components.CRect import CRect
from src.ecs.components.CColor import CColor
from src.ecs.components.CEnemySpawner import CEnemySpawner


def create_enemy(enemy_data):
    x = enemy_data.get("x", 0)
    y = enemy_data.get("y", 0)
    return {
        CPosition: CPosition(x, y),
        CVelocity: CVelocity(enemy_data["speed"]["x"], enemy_data["speed"]["y"]),
        CRect: CRect(enemy_data["size"]["w"], enemy_data["size"]["h"]),
        CColor: CColor(enemy_data["color"]["r"], enemy_data["color"]["g"], enemy_data["color"]["b"])
    }

def create_enemy_spawner(level_data):
    return {
        CEnemySpawner: CEnemySpawner(level_data)
    }
