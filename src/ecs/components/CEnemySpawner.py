import os
import json

class CEnemySpawner:
    def __init__(self, level_file: str):
        self.level_data = []
        self.timer = 0  # Control de tiempo para el spawn de enemigos
        self.load_level(level_file)

    def load_level(self, level_file: str):
        """Carga la configuración del nivel desde un JSON."""
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "assets", "cfg"))
        level_path = os.path.join(base_path, level_file)

        if not os.path.exists(level_path):
            print(f"❌ Error: ¡No se encontró el archivo {level_file}!")
            return

        with open(level_path, "r") as f:
            try:
                self.level_data = json.load(f).get("enemies", [])
            except json.JSONDecodeError as e:
                print(f"❌ Error al cargar JSON: {e}")
