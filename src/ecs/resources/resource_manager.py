import json
import pygame
from pathlib import Path
from typing import Dict, Any

class ResourceError(Exception):
    pass

class ResourceManager:
    def __init__(self):
        # La ruta base debe apuntar al directorio raíz del proyecto
        self.base_path = Path(__file__).parent.parent.parent.parent.parent
        self.assets_path = self.base_path / "assets"
        
    def load_image(self, image_name: str) -> pygame.Surface:
        path = self.assets_path / "img" / image_name
        if not path.exists():
            raise ResourceError(f"Image not found: {image_name}")
        return pygame.image.load(str(path)).convert_alpha()
        
    def load_config(self, config_name: str) -> Dict[str, Any]:
        path = self.assets_path / "cfg" / config_name
        if not path.exists():
            raise ResourceError(f"Config not found: {config_name}")
        with open(path) as f:
            return json.load(f)
            
    def get_default_config(self, config_type: str) -> Dict[str, Any]:
        defaults = {
            "player": {
                "image": "player.png",
                "health": 3,
                "velocity": {"vx": 0, "vy": 0},
                "animation": {"total_frames": 4, "frame_rate": 8}
            },
            "enemy": {
                "TypeA": {
                    "image": "enemy.png",
                    "health": 1,
                    "velocity": {"vx": 0, "vy": 50},
                    "animation": {"total_frames": 4, "frame_rate": 8}
                }
            },
            "hunter": {
                "image": "enemy.png",  # Usando enemy.png como default
                "health": 3,
                "velocity": {"vx": 0, "vy": 150},
                "detection_range": 200,
                "animation": {"total_frames": 4, "frame_rate": 8}
            },
            "bullet": {
                "image": "bullet.png",
                "health": 1,
                "velocity": {"vx": 0, "vy": -300}
            },
            "explosion": {
                "image": "explosion.png",
                "animation": {"total_frames": 4, "frame_rate": 8}
            }
        }
        return defaults.get(config_type, {}) 