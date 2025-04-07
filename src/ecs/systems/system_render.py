# src/ecs/systems/system_render.py
import pygame
from src.ecs.components.CPosition import CPosition
from src.ecs.components.CColor import CColor
from src.ecs.components.CRect import CRect

def system_render(entities, screen):
    for e in entities:
        pos = e.get(CPosition)
        color = e.get(CColor)
        rect = e.get(CRect)
        if pos and color and rect:
            pygame.draw.rect(screen, (color.r, color.g, color.b), pygame.Rect(pos.x, pos.y, rect.w, rect.h))
