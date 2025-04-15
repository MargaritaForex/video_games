import os
import json
import pygame

from src.ecs.systems.system_enemy_spawner import system_enemy_spawner
from src.ecs.systems.system_movement import system_movement
from src.ecs.systems.system_render import system_render
from src.ecs.systems.system_bullet_spawn import system_bullet_spawn, BulletSpawner
from src.ecs.systems.system_input import system_input
from src.ecs.systems.system_collision import system_collision
from src.ecs.entities.factory import create_enemy_components, create_player
from src.ecs.components.CHealth import CHealth

class GameEngine:
    def __init__(self) -> None:
        self.is_running = False
        self.screen = None
        self.clock = None
        self.width = 640
        self.height = 360
        self.bg_color = (0, 0, 0)
        self.fps = 60
        self.delta_time = 0.0
        self.score = 0

        # ECS
        self.entities = []
        self.player_entity = None
        self.bullet_cfg = None
        self.bullet_spawner = BulletSpawner()

    def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._render()
        self._clean()

    def _create(self):
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "assets", "cfg"))

        with open(os.path.join(base_path, "window.json"), "r") as f:
            window_cfg = json.load(f)["window"]
        with open(os.path.join(base_path, "level_01.json"), "r") as f:
            level_cfg = json.load(f)
        with open(os.path.join(base_path, "player.json"), "r") as f:
            player_cfg = json.load(f)
        with open(os.path.join(base_path, "bullet.json"), "r") as f:
            self.bullet_cfg = json.load(f)
        with open(os.path.join(base_path, "enemies.json"), "r") as f:
            enemies_cfg = json.load(f)

        self.width = window_cfg["size"]["w"]
        self.height = window_cfg["size"]["h"]
        self.bg_color = (
            window_cfg["bg_color"]["r"],
            window_cfg["bg_color"]["g"],
            window_cfg["bg_color"]["b"]
        )
        self.fps = window_cfg["framerate"]

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(window_cfg["title"])
        self.clock = pygame.time.Clock()

        # Create player
        player_position = level_cfg["player_spawn"]["position"]
        velocity = {"x": 0, "y": 0}
        self.player_entity = create_player(
            self,
            player_position,
            velocity,
            player_cfg["size"],
            player_cfg["color"]
        )
        
        # Add health component to player
        self.add_component(self.player_entity, CHealth(3))

        # Create enemy spawner
        spawner_entity = self.create_entity()
        spawner_components = create_enemy_components(level_cfg["enemy_spawn_events"], enemies_cfg)
        for c_type, component in spawner_components.items():
            self.add_component(spawner_entity, component)

    def _calculate_time(self):
        self.delta_time = self.clock.tick(self.fps) / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        # Handle input
        system_input(self.entities, self.player_entity, self)
        
        # Update game systems
        system_enemy_spawner(self, self.delta_time)
        system_movement(self.entities, self.width, self.height, self.delta_time)
        system_collision(self)
        
        # Handle shooting
        mouse_pressed = pygame.mouse.get_pressed()
        system_bullet_spawn(self, mouse_pressed, self.player_entity, self.bullet_cfg)
        
        # Check player health
        player_health = self.get_component(self.player_entity, CHealth)
        if player_health and player_health.current <= 0:
            self.is_running = False

    def _render(self):
        self.screen.fill(self.bg_color)
        system_render(self.entities, self.screen)
        
        # Render score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        
        # Render player health
        player_health = self.get_component(self.player_entity, CHealth)
        if player_health:
            health_text = font.render(f"Health: {player_health.current}", True, (255, 255, 255))
            self.screen.blit(health_text, (10, 50))
        
        pygame.display.flip()

    def _clean(self):
        pygame.quit()

    def create_entity(self):
        entity = len(self.entities)
        self.entities.append({})
        return entity

    def add_component(self, entity, component):
        self.entities[entity][type(component)] = component

    def get_component(self, entity, component_type):
        return self.entities[entity].get(component_type)

    def get_entities_with_components(self, *component_types):
        result = []
        for i, e in enumerate(self.entities):
            if all(ct in e for ct in component_types):
                result.append(i)
        return result
