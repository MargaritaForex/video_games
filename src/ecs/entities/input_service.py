import pygame
from src.ecs.components.CVelocity import CVelocity

class Command:
    def execute(self, entity, world):
        pass

class MoveUpCommand(Command):
    def execute(self, entity, world):
        vel = world.get_component(entity, CVelocity)
        vel.vy = -100

class MoveDownCommand(Command):
    def execute(self, entity, world):
        vel = world.get_component(entity, CVelocity)
        vel.vy = 100

class MoveLeftCommand(Command):
    def execute(self, entity, world):
        vel = world.get_component(entity, CVelocity)
        vel.vx = -100

class MoveRightCommand(Command):
    def execute(self, entity, world):
        vel = world.get_component(entity, CVelocity)
        vel.vx = 100

class InputService:
    def __init__(self):
        self._key_command_map = {
            pygame.K_w: MoveUpCommand(),
            pygame.K_s: MoveDownCommand(),
            pygame.K_a: MoveLeftCommand(),
            pygame.K_d: MoveRightCommand()
        }

    def get_commands(self):
        keys = pygame.key.get_pressed()
        return [cmd for key, cmd in self._key_command_map.items() if keys[key]]
