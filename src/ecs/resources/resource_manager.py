import json
import pygame
from pathlib import Path
from typing import Dict, Any

class ResourceError(Exception):
    """Excepción personalizada para errores de carga de recursos."""
    pass


class ResourceManager:
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.base_path = Path(__file__).resolve().parent.parent.parent.parent
        self.assets_path = self.base_path / "assets"
        self.img_path = self.assets_path / "img"
        self.cfg_path = self.assets_path / "cfg"

        if self.debug:
            self._print_paths()

    def _print_paths(self):
        print(f"Base path: {self.base_path}")
        print(f"Assets path: {self.assets_path} (Exists: {self.assets_path.exists()})")
        print(f"Img path: {self.img_path} (Exists: {self.img_path.exists()})")
        print(f"Cfg path: {self.cfg_path} (Exists: {self.cfg_path.exists()})")

    def load_image(self, image_name: str) -> pygame.Surface:
        path = self._get_asset_path(image_name, self.img_path)
        self._check_exists(path, f"Image not found: {image_name}")
        return pygame.image.load(str(path)).convert_alpha()

    def load_config(self, config_name: str) -> Dict[str, Any]:
        path = self._get_asset_path(config_name, self.cfg_path)
        self._check_exists(path, f"Config not found: {config_name}")
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
                "image": "enemy.png",
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

    def _get_asset_path(self, name: str, base: Path) -> Path:
        return (base / name) if "/" not in name else (self.assets_path / name)

    def _check_exists(self, path: Path, error_msg: str):
        if not path.exists():
            raise ResourceError(error_msg)
