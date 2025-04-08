#!/usr/bin/python3
"""Función Main"""

from src.engine.game_engine import GameEngine
from src.ecs.components.CBullet import CBullet

if __name__ == "__main__":
    engine = GameEngine()
    engine.run()
