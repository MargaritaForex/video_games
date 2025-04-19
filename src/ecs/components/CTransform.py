class CTransform:
    def __init__(self, x: float, y: float):
        self.pos = type('Point', (), {'x': x, 'y': y}) 