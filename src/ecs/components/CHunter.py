class CHunter:
    def __init__(self, chase_distance: float, return_distance: float, chase_speed: float):
        self.chase_distance = chase_distance
        self.return_distance = return_distance
        self.chase_speed = chase_speed
        self.origin = None
        self.is_chasing = False
        self.is_returning = False 