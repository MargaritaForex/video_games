# src/ecs/entities/factory.py
from src.ecs.components.CPosition import CPosition
from src.ecs.components.CVelocity import CVelocity
from src.ecs.components.CEnemySpawner import CEnemySpawner
from src.ecs.components.CSurface import CSurface
from src.ecs.components.CAnimation import CAnimation
import random
import os

def create_enemy(world, pos, cfg):
    entity = world.create_entity()
    
    # Crear componentes básicos
    world.add_component(entity, CPosition(pos["x"], pos["y"]))
    world.add_component(entity, CVelocity(0, random.randint(cfg["velocity_min"], cfg["velocity_max"])))
    
    # Crear sprite
    image_path = get_image_path(cfg["image"])
    world.add_component(entity, CSurface(image_path))
    
    return entity

def create_enemy_components(enemy_events, enemy_types_data):
    return {
        CEnemySpawner: CEnemySpawner(enemy_events, enemy_types_data)
    }

def get_image_path(image_name):
    # Obtener la ruta base del proyecto
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    # Construir la ruta completa de la imagen
    return os.path.join(base_path, "assets", "img", image_name)

def create_player(world, pos, vel, cfg):
    entity = world.create_entity()
    
    # Crear componentes básicos
    world.add_component(entity, CPosition(pos["x"], pos["y"]))
    world.add_component(entity, CVelocity(vel["vx"], vel["vy"]))
    
    # Crear sprite y animación
    image_path = get_image_path(cfg["image"])
    world.add_component(entity, CSurface(image_path))
    
    if "animations" in cfg:
        world.add_component(entity, CAnimation(
            num_frames=cfg["num_frames"],
            animations=cfg["animations"]
        ))
        
    return entity

def create_bullet(world, pos, cfg):
    entity = world.create_entity()
    
    # Crear componentes básicos
    world.add_component(entity, CPosition(pos.x, pos.y))
    world.add_component(entity, CVelocity(cfg["velocity"]["vx"], cfg["velocity"]["vy"]))
    
    # Crear sprite
    image_path = get_image_path(cfg["image"])
    world.add_component(entity, CSurface(image_path))
    
    return entity
