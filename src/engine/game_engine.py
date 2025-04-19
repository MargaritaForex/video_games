import os
import json
import pygame
from src.ecs.constants import VELOCITY_X, VELOCITY_Y

from src.ecs.systems.system_enemy_spawner import system_enemy_spawner
from src.ecs.systems.system_movement import system_movement
from src.ecs.systems.system_render import system_render
from src.ecs.systems.system_input import system_input
from src.ecs.systems.system_collision import system_collision
from src.ecs.systems.system_animation import system_animation
from src.ecs.systems.system_hunter import system_hunter
from src.ecs.systems.system_explosion import system_explosion
from src.create.prefab_creator import PrefabCreator

class GameEngine:
    def __init__(self) -> None:
        self.player_spawn_position = None
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
        self.entities = {}
        self.player_entity = None
        self.bullet_cfg = None
        self.prefab_creator = PrefabCreator(self)

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
        self.player_spawn_position = level_cfg["player_spawn"]["position"]
        with open(os.path.join(base_path, "player.json"), "r") as f:
            player_cfg = json.load(f)
        with open(os.path.join(base_path, "bullet.json"), "r") as f:
            self.bullet_cfg = json.load(f)

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
        velocity = {VELOCITY_X: 0, VELOCITY_Y: 0}
        self.player_entity = self.prefab_creator.create_player(player_position, velocity, player_cfg)

        # Create enemy spawner
        self.prefab_creator.create_enemy_spawner()

    def _calculate_time(self):
        self.delta_time = self.clock.tick(self.fps) / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        self.delta_time = self.clock.tick(self.fps) / 1000.0
        
        # Actualizar sistemas
        system_input(self)
        system_movement(self.entities, self.width, self.height, self.delta_time)
        system_collision(self.entities, self.prefab_creator)
        system_animation(self.entities, self.delta_time)
        system_hunter(self.entities, self.player_entity, self.delta_time)
        system_explosion(self.entities, self.delta_time)
        system_enemy_spawner(self, self.prefab_creator, self.delta_time)
        
        # Renderizar
        self._render()

    def _render(self):
        self.screen.fill(self.bg_color)
        system_render(self.entities, self.screen)

        # Renderizar score (si lo necesitas)
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

        pygame.display.flip()

    def _clean(self):
        pygame.quit()

    def create_entity(self):
        entity = len(self.entities)
        self.entities[entity] = {}
        return entity

    def add_component(self, entity, component):
        self.entities[entity][type(component)] = component

    def get_component(self, entity, component_type):
        return self.entities[entity].get(component_type)

    def get_entities_with_components(self, *component_types):
        result = []
        for entity_id, components in self.entities.items():
            if all(ct in components for ct in component_types):
                result.append(entity_id)
        return result
