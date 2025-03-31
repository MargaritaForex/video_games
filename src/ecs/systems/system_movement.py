class SystemMovement:
    def __init__(self, entities, screen_width, screen_height):
        """Sistema que maneja el movimiento de los enemigos."""
        self.entities = entities
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self, delta_time):
        """Actualiza la posición de todos los enemigos."""
        for entity in self.entities:
            if hasattr(entity, "move"):
                entity.move(self.screen_width, self.screen_height)
