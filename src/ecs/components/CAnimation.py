class Animation:
    def __init__(self, start_frame: int, end_frame: int, framerate: float):
        self.start_frame = start_frame
        self.end_frame = end_frame
        self.framerate = framerate
        self.current_frame = start_frame
        self.time_since_last_frame = 0.0
        self.finished = False  # 👈 ESTO ES LO QUE FALTABA

class CAnimation:
    def __init__(self, num_frames: int, animations: dict):
        self.num_frames = num_frames
        self.animations = {name: Animation(**data) for name, data in animations.items()}
        self.current_animation = None
        self.frame_width = 0  # Se establecerá cuando se cargue la textura
        
    def set_animation(self, name: str):
        if name in self.animations:
            self.current_animation = self.animations[name]
            self.current_animation.current_frame = self.current_animation.start_frame
            self.current_animation.time_since_last_frame = 0.0
            
    def update(self, delta_time: float):
        if self.current_animation:
            self.current_animation.time_since_last_frame += delta_time
            frame_duration = 1.0 / self.current_animation.framerate
            
            if self.current_animation.time_since_last_frame >= frame_duration:
                self.current_animation.time_since_last_frame = 0.0
                self.current_animation.current_frame += 1
                
                if self.current_animation.current_frame > self.current_animation.end_frame:
                    self.current_animation.current_frame = self.current_animation.start_frame
                    
    def get_current_frame(self) -> int:
        return self.current_animation.current_frame if self.current_animation else 0

    def is_done(self) -> bool:
        return self.current_animation.finished if self.current_animation else False