import pygame
from src.ecs.resources.resource_manager import ResourceManager

class CSurface:
    def __init__(self, image: pygame.Surface):
        self.surface = image
        self.area = self.surface.get_rect()
        self.original_surface = self.surface.copy()
        
    def get_rect(self):
        return self.area.copy()
    
    def get_surface(self):
        return self.surface 