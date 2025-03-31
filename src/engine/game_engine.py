import os
import json
import pygame


class GameEngine:
    def __init__(self) -> None:
        self.is_running = False
        self.screen = None
        self.clock = None
        self.width = 640
        self.height = 360
        self.bg_color = (0, 0, 0)
        self.fps = 60

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
        """Carga la configuración de la ventana y inicializa Pygame."""
        base_path = os.path.join(os.path.dirname(__file__), "..", "assets", "cfg")
        config_path = os.path.join(base_path, "window.json")

        # Cargar configuración desde JSON
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                config = json.load(f)

            window_config = config["window"]
            self.width = window_config["size"]["w"]
            self.height = window_config["size"]["h"]
            self.bg_color = (
                window_config["bg_color"]["r"],
                window_config["bg_color"]["g"],
                window_config["bg_color"]["b"]
            )
            self.fps = window_config["framerate"]

        # Inicializar Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(window_config["title"])
        self.clock = pygame.time.Clock()

    def _calculate_time(self):
        """Control del tiempo de actualización."""
        self.clock.tick(self.fps)

    def _process_events(self):
        """Manejo de eventos de entrada."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        """Actualizar lógica del juego."""
        pass  # Aquí puedes agregar lógica de actualización más adelante

    def _draw(self):
        """Dibuja en la pantalla."""
        self.screen.fill(self.bg_color)
        pygame.display.flip()

    def _clean(self):
        """Limpia y cierra el juego."""
        pygame.quit()
