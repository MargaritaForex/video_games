import pygame

class SystemRender:
    def __init__(self, screen, entities: list):
        self.screen = screen
        self.entities = entities

    def render(self):
        """Dibuja los enemigos en la pantalla."""
        for entity in self.entities:
            if hasattr(entity, "rect"):
                pygame.draw.rect(
                    self.screen,
                    entity.color,
                    entity.rect  # 📌 Se usa `entity.rect` en lugar de `entity.x, entity.y`
                )
