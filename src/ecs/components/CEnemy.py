import pygame

class CEnemy:
    def __init__(self, x, y, w, h, speed_x, speed_y, color):
        """Inicializa un enemigo con posición, tamaño, velocidad y color."""
        self.rect = pygame.Rect(x, y, w, h)
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.color = color  # Color en formato (r, g, b)

    def move(self, screen_width, screen_height):
        """Mueve al enemigo y hace que rebote en los bordes de la pantalla."""
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # 📌 Rebotar en los bordes
        if self.rect.left <= 0 or self.rect.right >= screen_width:
            self.speed_x *= -1  # Invierte la dirección en X
        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            self.speed_y *= -1  # Invierte la dirección en Y

    def draw(self, screen):
        """Dibuja el enemigo en la pantalla."""
        pygame.draw.rect(screen, self.color, self.rect)
