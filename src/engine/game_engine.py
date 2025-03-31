import os
import json
import pygame

from src.ecs.systems.system_enemy_spawner import SystemEnemySpawner
from src.ecs.systems.system_movement import SystemMovement
from src.ecs.systems.system_render import SystemRender


class GameEngine:
    def __init__(self) -> None:
        self.is_running = False
        self.screen = None
        self.clock = None
        self.width = 640
        self.height = 360
        self.bg_color = (0, 0, 0)
        self.fps = 60

        # 📌 Agregar variables ECS
        self.entities = []
        self.enemy_spawner = None
        self.system_movement = None
        self.system_render = None

    def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
        self._clean()

    def _create(self):
        """Carga la configuración de la ventana y ECS."""
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "assets", "cfg"))
        config_path = os.path.join(base_path, "window.json")
        level_path = os.path.join(base_path, "level_01.json")  # 📌 Cargar nivel

        # Cargar configuración de ventana
        if not os.path.exists(config_path):
            print("❌ Error: ¡No se encontró el archivo window.json!")
            exit(1)
        with open(config_path, "r") as f:
            config = json.load(f)

        window_config = config.get("window", {})
        self.width = window_config.get("size", {}).get("w", 640)
        self.height = window_config.get("size", {}).get("h", 360)
        self.bg_color = (
            window_config.get("bg_color", {}).get("r", 0),
            window_config.get("bg_color", {}).get("g", 0),
            window_config.get("bg_color", {}).get("b", 0)
        )
        self.fps = window_config.get("framerate", 60)

        # Inicializar Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(window_config.get("title", "Juego sin título"))
        self.clock = pygame.time.Clock()

        # 📌 Cargar nivel
        if not os.path.exists(level_path):
            print("❌ Error: ¡No se encontró el archivo level_01.json!")
            exit(1)
        with open(level_path, "r") as f:
            level_data = json.load(f)

        # 📌 Inicializar sistemas ECS
        self.enemy_spawner = SystemEnemySpawner(level_data.get("enemies", []), self.entities)
        self.system_movement = SystemMovement(self.entities, self.width, self.height)
        self.system_render = SystemRender(self.screen, self.entities)

    def _calculate_time(self):
        """Control del tiempo de actualización."""
        self.delta_time = self.clock.tick(self.fps) / 1000.0  # Convertir a segundos

    def _process_events(self):
        """Manejo de eventos de entrada."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        """Actualizar lógica del juego."""
        self.enemy_spawner.update(self.delta_time)
        self.system_movement.update(self.delta_time)

    def _draw(self):
        """Dibuja en la pantalla."""
        self.screen.fill(self.bg_color)

        # 📌 Dibujar enemigos usando el método `draw()`
        for entity in self.entities:
            if hasattr(entity, "draw"):
                entity.draw(self.screen)

        pygame.display.flip()

    def _clean(self):
        """Limpia y cierra el juego."""
        pygame.quit()
