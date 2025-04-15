import pygame

class CSurface:
    def __init__(self, image_path: str, area: pygame.Rect = None):
        self.surface = pygame.image.load(image_path).convert_alpha()
        self.area = area if area else self.surface.get_rect()
        self.original_surface = self.surface.copy()
        
    def get_rect(self):
        return self.area.copy()
    
    def get_surface(self):
        return self.surface 