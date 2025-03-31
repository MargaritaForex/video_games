class SystemMovement:
    def __init__(self, entities: list, screen_width: int, screen_height: int):
        self.entities = entities
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self, delta_time):
        """Actualiza la posición de los enemigos en la pantalla."""
        for entity in self.entities:
            if hasattr(entity, "speed_x") and hasattr(entity, "speed_y"):
                entity.x += entity.speed_x * delta_time
                entity.y += entity.speed_y * delta_time

                # Rebotar en los bordes
                if entity.x <= 0 or entity.x + entity.w >= self.screen_width:
                    entity.speed_x *= -1  # Invierte la dirección en X
                if entity.y <= 0 or entity.y + entity.h >= self.screen_height:
                    entity.speed_y *= -1  # Invierte la dirección en Y
