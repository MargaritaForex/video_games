class CEnemySpawner:
    type_name = "CEnemySpawner"
    
    @classmethod
    def create(cls, spawner_cfg: dict) -> dict:
        return {
            "time_to_spawn": spawner_cfg["time_to_spawn"],
            "current_time": 0,
            "spawn_points": spawner_cfg["spawn_points"]
        } 