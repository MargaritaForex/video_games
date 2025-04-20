import json
from pathlib import Path
from typing import Dict

from src.ecs.components.CAnimation import CAnimation
from src.ecs.components.CSurface import CSurface
from src.ecs.components.CPosition import CPosition
from src.ecs.components.CVelocity import CVelocity
from src.ecs.components.CEnemySpawner import CEnemySpawner
from src.ecs.components.CHunter import CHunter
from src.create.prefab_creator_interface import IPrefabCreator
from src.ecs.resources.resource_manager import ResourceManager, ResourceError

class PrefabCreator(IPrefabCreator):
    def __init__(self, entity_manager):
        self._entity_manager = entity_manager
        self._resource_manager = ResourceManager()
        self._load_configs()

    def _load_configs(self):
        try:
            self._enemy_data = self._resource_manager.load_config("enemy.json")
        except ResourceError:
            self._enemy_data = self._resource_manager.get_default_config("enemy")
            
        try:
            self._hunter_data = self._resource_manager.load_config("hunter.json")
        except ResourceError:
            self._hunter_data = self._resource_manager.get_default_config("hunter")
            
        try:
            self._spawner_data = self._resource_manager.load_config("enemy_spawner.json")
        except ResourceError:
            self._spawner_data = {"spawn_points": []}
            
        try:
            self._bullet_data = self._resource_manager.load_config("bullet.json")
        except ResourceError:
            self._bullet_data = self._resource_manager.get_default_config("bullet")
            
        try:
            self._explosion_data = self._resource_manager.load_config("explosion.json")
        except ResourceError:
            self._explosion_data = self._resource_manager.get_default_config("explosion")

    def _build_surface_with_animation_area(self, image, num_frames):
        import pygame
        frame_width = image.get_width() // num_frames
        frame_height = image.get_height()
        surface = CSurface(image)
        surface.area = pygame.Rect(0, 0, frame_width, frame_height)
        return surface

    def create_player(self, position: Dict[str, float], velocity: Dict[str, float], player_cfg: Dict) -> int:
        required_keys = ["image", "health"]
        if not all(key in player_cfg for key in required_keys):
            player_cfg = self._resource_manager.get_default_config("player")
            
        player_ent = self._entity_manager.create_entity()
        
        try:
            image = self._resource_manager.load_image(player_cfg["image"])
            if "animation" in player_cfg:
                anim_cfg = player_cfg["animation"]
                surface = self._build_surface_with_animation_area(image, anim_cfg["total_frames"])
            else:
                surface = CSurface(image)

            self._entity_manager.add_component(player_ent, surface)
        except ResourceError:
            print(f"Warning: Could not load player image. Using default.")
            image = self._resource_manager.load_image("player.png")
            if "animation" in player_cfg:
                anim_cfg = player_cfg["animation"]
                surface = self._build_surface_with_animation_area(image, anim_cfg["total_frames"])
            else:
                surface = CSurface(image)

            self._entity_manager.add_component(player_ent, surface)
            
        self._entity_manager.add_component(player_ent,
            CPosition(position["x"], position["y"]))
        self._entity_manager.add_component(player_ent,
            CVelocity(velocity["vx"], velocity["vy"]))
        
        if "animation" in player_cfg:
            anim_cfg = player_cfg["animation"]
            animations = {
                "default": {
                    "start_frame": 0,
                    "end_frame": anim_cfg["total_frames"] - 1,
                    "framerate": anim_cfg["frame_rate"]
                }
            }
            animation = CAnimation(anim_cfg["total_frames"], animations)
            animation.set_animation("default")
            self._entity_manager.add_component(player_ent, animation)
        
        return player_ent

    def create_enemy(self, position: Dict[str, float], enemy_type: str) -> int:
        print(f"🧪 Creando enemigo con tipo: {enemy_type}")
        print(f"✅ Enemigo creado: {enemy_type} en {position}")
        if enemy_type not in self._enemy_data:
            print(f"Warning: Enemy type {enemy_type} not found. Using default.")
            enemy_cfg = self._resource_manager.get_default_config("enemy")["TypeA"]
        else:
            enemy_cfg = self._enemy_data[enemy_type]
            
        enemy_ent = self._entity_manager.create_entity()
        
        try:
            image = self._resource_manager.load_image(enemy_cfg["image"])
            self._entity_manager.add_component(enemy_ent, CSurface(image))
        except ResourceError:
            print(f"Warning: Could not load enemy image. Using default.")
            image = self._resource_manager.load_image("enemy.png")
            self._entity_manager.add_component(enemy_ent, CSurface(image))
            
        self._entity_manager.add_component(enemy_ent,
            CPosition(position["x"], position["y"]))
        self._entity_manager.add_component(enemy_ent,
            CVelocity(enemy_cfg["velocity"]["vx"], enemy_cfg["velocity"]["vy"]))
        
        if "animation" in enemy_cfg:
            anim_cfg = enemy_cfg["animation"]
            animations = {
                "default": {
                    "start_frame": 0,
                    "end_frame": anim_cfg["total_frames"] - 1,
                    "framerate": anim_cfg["frame_rate"]
                }
            }
            self._entity_manager.add_component(enemy_ent,
                CAnimation(anim_cfg["total_frames"], animations))
        
        return enemy_ent

    def create_hunter(self, position: Dict[str, float]) -> int:
        hunter_ent = self._entity_manager.create_entity()
        
        try:
            image = self._resource_manager.load_image(self._hunter_data["image"])
            self._entity_manager.add_component(hunter_ent, CSurface(image))
        except ResourceError:
            print(f"Warning: Could not load hunter image. Using default.")
            image = self._resource_manager.load_image("enemy.png")
            self._entity_manager.add_component(hunter_ent, CSurface(image))
            
        self._entity_manager.add_component(hunter_ent,
            CPosition(position["x"], position["y"]))
        self._entity_manager.add_component(hunter_ent,
            CVelocity(self._hunter_data["velocity"]["vx"], 
                     self._hunter_data["velocity"]["vy"]))
        self._entity_manager.add_component(hunter_ent,
            CHunter(self._hunter_data["detection_range"]))
        
        if "animation" in self._hunter_data:
            anim_cfg = self._hunter_data["animation"]
            animations = {
                "default": {
                    "start_frame": 0,
                    "end_frame": anim_cfg["total_frames"] - 1,
                    "framerate": anim_cfg["frame_rate"]
                }
            }
            self._entity_manager.add_component(hunter_ent,
                CAnimation(anim_cfg["total_frames"], animations))
        
        return hunter_ent

    def create_enemy_spawner(self) -> int:
        spawner_ent = self._entity_manager.create_entity()
        
        # Convertir los spawn_points al formato esperado por el sistema
        level_data = []
        for spawn_point in self._spawner_data["spawn_points"]:
            level_data.append({
                "time": spawn_point["time"],
                "position": spawn_point["position"],
                "enemy_type": spawn_point["enemy_type"]
            })
        
        self._entity_manager.add_component(spawner_ent,
            CEnemySpawner(level_data, self._enemy_data))
        
        return spawner_ent

    def create_explosion(self, position: Dict[str, float]) -> int:
        explosion_ent = self._entity_manager.create_entity()

        try:
            image = self._resource_manager.load_image(self._explosion_data["image"])
            self._entity_manager.add_component(explosion_ent, CSurface(image))
        except ResourceError:
            print(f"Warning: Could not load explosion image. Using default.")
            image = self._resource_manager.load_image("explosion.png")
            self._entity_manager.add_component(explosion_ent, CSurface(image))

        self._entity_manager.add_component(explosion_ent,
                                           CPosition(position["x"], position["y"]))

        # ➕ Agregamos el componente de explosión
        from src.ecs.components.CExplosion import CExplosion
        self._entity_manager.add_component(explosion_ent, CExplosion(0.5))  # o el valor que consideres

        try:
            num_frames = self._explosion_data["animations"]["number_frames"]
            anim_list = self._explosion_data["animations"]["list"]
            animations = {}
            for anim in anim_list:
                animations[anim["name"]] = {
                    "start_frame": anim["start"],
                    "end_frame": anim["end"],
                    "framerate": anim["framerate"]
                }
            animation = CAnimation(num_frames, animations)
            animation.set_animation("EXPLODE")  # Asegúrate que "EXPLODE" esté en tu JSON
            self._entity_manager.add_component(explosion_ent, animation)
        except Exception as e:
            print(f"Error loading explosion animation: {e}")

        return explosion_ent


    def get_default_player_cfg(self):
        try:
            return self._resource_manager.load_config("player.json")
        except ResourceError:
            return self._resource_manager.get_default_config("player")

