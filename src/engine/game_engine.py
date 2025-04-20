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
from src.ecs.systems.system_mouse_input import system_mouse_input

class GameEngine:
    def __init__(self) -> None:
        self.entities = {}
        self.player_entity = None
        self.player_spawn_position = None
        self.bullet_cfg = None

        self.screen = None
        self.clock = None
        self.width = 640
        self.height = 360
        self.bg_color = (0, 0, 0)
        self.fps = 60
        self.delta_time = 0.0
        self.is_running = False

        self.prefab_creator = PrefabCreator(self)

    def run(self) -> None:
        self._create()
        self._game_loop()
        self._clean()

    def _game_loop(self):
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._render()

    def _load_configs(self):
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "assets", "cfg"))
        with open(os.path.join(base_path, "window.json"), "r") as f:
            return {
                "window_cfg": json.load(f)["window"],
                "level_cfg": json.load(open(os.path.join(base_path, "level_01.json"))),
                "player_cfg": json.load(open(os.path.join(base_path, "player.json"))),
                "bullet_cfg": json.load(open(os.path.join(base_path, "bullet.json"))),
            }

    def _setup_window(self, window_cfg):
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

    def _create(self):
        cfg = self._load_configs()
        self._setup_window(cfg["window_cfg"])

        self.player_spawn_position = cfg["level_cfg"]["player_spawn"]["position"]
        self.bullet_cfg = cfg["bullet_cfg"]

        velocity = {VELOCITY_X: 0, VELOCITY_Y: 0}
        self.player_entity = self.prefab_creator.create_player(
            self.player_spawn_position, velocity, cfg["player_cfg"]
        )
        self.prefab_creator.create_initial_static_enemies()
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
        system_mouse_input(self)
        system_movement(self.entities, self.width, self.height, self.delta_time)
        system_collision(self.entities, self.prefab_creator)
        system_animation(self.entities, self.delta_time)
        system_hunter(self.entities, self.player_entity, self.delta_time)
        system_explosion(self.entities, self.delta_time)
        system_enemy_spawner(self, self.prefab_creator, self.delta_time)

    def _render(self):
        self.screen.fill(self.bg_color)
        system_render(self.entities, self.screen)

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
        return [eid for eid, comps in self.entities.items() if all(ct in comps for ct in component_types)]
