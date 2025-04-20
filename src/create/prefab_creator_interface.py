from abc import ABC, abstractmethod
from typing import Dict

class IPrefabCreator(ABC):
    @abstractmethod
    def create_player(self, position: Dict[str, float], velocity: Dict[str, float], player_cfg: Dict) -> int:
        pass
