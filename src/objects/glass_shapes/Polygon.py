class Polygon:
    def __init__(self, 
                 vertices: list[tuple[int, int]], 
                 position: tuple[int, int],
                 refractive_index: float,
                 ):
        self.vertices = vertices
        self.position = position
        self.refractive_index = refractive_index