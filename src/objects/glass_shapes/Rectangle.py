from objects.glass_shapes.Polygon import Polygon

class Rectangle(Polygon):
    def __init__(self, 
                 width: int, 
                 height: int, 
                 position: tuple[int, int],
                 refractive_index: float,
                 ):
        self.width = width
        self.height = height
        self.position = position #defined as top left point of the rectangle
        self.refractive_index = refractive_index
        vertices = [
            (position[0], position[1]),  # top-left
            (position[0] + width, position[1]),  # top-right
            (position[0] + width, position[1] + height),  # bottom-right
            (position[0], position[1] + height)  # bottom-left
        ]
        super().__init__(vertices, position, refractive_index)
        self.vertices = vertices

    def get_vertices(self):
        return self.vertices

    # this subroutine ensures that the rectangle stays as a rectangle when updating points, instead of allowing it to turn into a general polygon
    def update_size(self, point: tuple[int, int], point_type: str):
        # clamp the point to ensure that the rectangle does not become inverted, and has a size of at least 3 pixels
        if point_type == "tl": # top-left
            point = (min(point[0], self.position[0] + self.width - 3), min(point[1], self.position[1] + self.height - 3))
        elif point_type == "tr": # top-right
            point = (max(point[0], self.position[0]+3), min(point[1], self.position[1] + self.height - 3))
        elif point_type == "br": # bottom-right
            point = (max(point[0], self.position[0]+3), max(point[1], self.position[1]+3))
        elif point_type == "bl": # bottom-left
            point = (min(point[0], self.position[0] + self.width - 3), max(point[1], self.position[1]+3))
        else:
            raise ValueError("Invalid point_type. Must be one of 'tl', 'tr', 'br', 'bl'.")
        
        match point_type:
            case "tl": # top-left
                # deduce new width and height based on the new top-left point
                self.width = self.width + (self.position[0] - point[0])
                self.height = self.height + (self.position[1] - point[1])
                self.position = point # change the top left point
            case "tr": # top-right
                # deduce new width and height based on the new top-right point
                self.width = point[0] - self.position[0]
                self.height = self.height + (self.position[1] - point[1])
                self.position = (self.position[0], point[1]) # change the top left point's y-coordinate
            case "br": # bottom-right
                # deduce new width and height based on the new bottom-right point
                self.width = point[0] - self.position[0]
                self.height = point[1] - self.position[1]
                # do not need to change the position of the top left point
            case "bl": # bottom-left
                # deduce new width and height based on the new bottom-left point
                self.width = self.width + (self.position[0] - point[0])
                self.height = point[1] - self.position[1]
                self.position = (point[0], self.position[1]) # change the top left point's x-coordinate

        # update the new vertices based on the new position, width and height
        self.vertices = [
            (self.position[0], self.position[1]),  # top-left
            (self.position[0] + self.width, self.position[1]),  # top-right
            (self.position[0] + self.width, self.position[1] + self.height),  # bottom-right
            (self.position[0], self.position[1] + self.height)  # bottom-left
        ]