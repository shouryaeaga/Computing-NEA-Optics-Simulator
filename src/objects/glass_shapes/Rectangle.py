from src.objects.glass_shapes.Polygon import Polygon


class Rectangle(Polygon):
    def __init__(self, 
                 width: int, 
                 height: int, 
                 position: tuple[int, int],
                 refractive_index: float,
                 ):
        self.width = width
        self.height = height
        self.position = position
        self.refractive_index = refractive_index
        vertices = [
            (position[0] - width // 2, position[1] - height // 2),  # Top-left
            (position[0] + width // 2, position[1] - height // 2),  # Top-right
            (position[0] + width // 2, position[1] + height // 2),  # Bottom-right
            (position[0] - width // 2, position[1] + height // 2),  # Bottom-left
        ]
        super().__init__(vertices, position, refractive_index)

    def get_vertices(self):
        return self.vertices