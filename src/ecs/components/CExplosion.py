class CExplosion:
    def __init__(self, duration: float):
        self.duration = duration
        self.time_elapsed = 0.0
        self.is_finished = False 