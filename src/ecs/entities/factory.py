# src/ecs/entities/factory.py
from src.ecs.components.CBullet import CBullet
from src.ecs.components.CPosition import CPosition
from src.ecs.components.CVelocity import CVelocity
from src.ecs.components.CEnemySpawner import CEnemySpawner
from src.ecs.components.CSurface import CSurface
from src.ecs.components.CAnimation import CAnimation
from src.ecs.components.CHealth import CHealth
from src.ecs.components.CHunter import CHunter
from src.ecs.components.CExplosion import CExplosion
import random
import os

def create_enemy(world, pos, cfg):
    entity = world.create_entity()
    
    # Crear componentes básicos
    world.add_component(entity, CPosition(pos["x"], pos["y"]))
    world.add_component(entity, CVelocity(0, random.randint(cfg["velocity_min"], cfg["velocity_max"])))
    world.add_component(entity, CHealth(cfg["health"]))
    
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
    world.add_component(entity, CHealth(3))
    
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
    world.add_component(entity, CHealth(cfg["health"]))
    
    # Crear sprite
    image_path = get_image_path(cfg["image"])
    world.add_component(entity, CSurface(image_path))
    
    return entity

def create_hunter(world, pos, cfg):
    entity = world.create_entity()
    
    # Crear componentes básicos
    world.add_component(entity, CPosition(pos["x"], pos["y"]))
    world.add_component(entity, CVelocity(0, 0))
    world.add_component(entity, CHealth(cfg["health"]))
    world.add_component(entity, CHunter(
        chase_distance=cfg["chase_distance"],
        return_distance=cfg["return_distance"],
        chase_speed=cfg["chase_speed"]
    ))
    
    # Crear sprite y animación
    image_path = get_image_path(cfg["image"])
    world.add_component(entity, CSurface(image_path))
    
    if "animations" in cfg:
        world.add_component(entity, CAnimation(
            num_frames=cfg["num_frames"],
            animations=cfg["animations"]
        ))
        
    return entity

def create_explosion(world, pos):
    entity = world.create_entity()
    
    # Crear componentes básicos
    world.add_component(entity, CPosition(pos["x"], pos["y"]))
    world.add_component(entity, CExplosion(0.5))  # Duración de 0.5 segundos
    
    # Crear sprite y animación
    image_path = get_image_path("explosion.png")
    world.add_component(entity, CSurface(image_path))
    
    # Configurar animación de explosión
    world.add_component(entity, CAnimation(
        num_frames=8,
        animations={
            "EXPLODE": {
                "start_frame": 0,
                "end_frame": 7,
                "framerate": 16
            }
        }
    ))
    
    return entity