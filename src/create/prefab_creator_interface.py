from abc import ABC, abstractmethod
from typing import Dict

class IPrefabCreator(ABC):
    @abstractmethod
    def create_player(self, position: Dict[str, float], velocity: Dict[str, float], player_cfg: Dict) -> int:
        pass

    @abstractmethod
    def create_enemy(self, position: Dict[str, float], enemy_type: str) -> int:
        pass

    @abstractmethod
    def create_hunter(self, position: Dict[str, float]) -> int:
        pass

    @abstractmethod
    def create_enemy_spawner(self) -> int:
        pass

    @abstractmethod
    def create_explosion(self, position: Dict[str, float]) -> int:
        pass

    @abstractmethod
    def create_bullet(self, position: Dict[str, float]) -> int:
        pass 