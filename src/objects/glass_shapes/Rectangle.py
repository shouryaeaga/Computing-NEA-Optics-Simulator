from objects.glass_shapes.Polygon import Polygon

class Rectangle(Polygon):
    def __init__(self, 
                 width: int, 
                 height: int, 
                 position: tuple[int, int],
                 refractive_index: float,
                 ):
        self.__width = width
        self.__height = height
        self.__position = position
        vertices = [
            (position[0], position[1]),  # top-left
            (position[0] + width, position[1]),  # top-right
            (position[0] + width, position[1] + height),  # bottom-right
            (position[0], position[1] + height)  # bottom-left
        ]
        super().__init__(vertices, position, refractive_index)
        self.__vertices = vertices

    def get_vertices(self):
        return self.__vertices

    # this subroutine ensures that the rectangle stays as a rectangle when updating points, instead of allowing it to turn into a general polygon
    def update_size(self, point: tuple[int, int], point_type: str):
        # clamp the point to ensure that the rectangle does not become inverted, and has a size of at least 3 pixels
        if point_type == "tl": # top-left
            point = (min(point[0], self.__position[0] + self.__width - 3), min(point[1], self.__position[1] + self.__height - 3))
        elif point_type == "tr": # top-right
            point = (max(point[0], self.__position[0]+3), min(point[1], self.__position[1] + self.__height - 3))
        elif point_type == "br": # bottom-right
            point = (max(point[0], self.__position[0]+3), max(point[1], self.__position[1]+3))
        elif point_type == "bl": # bottom-left
            point = (min(point[0], self.__position[0] + self.__width - 3), max(point[1], self.__position[1]+3))
        else:
            raise ValueError("Invalid point_type. Must be one of 'tl', 'tr', 'br', 'bl'.")
        
        match point_type:
            case "tl": # top-left
                # deduce new width and height based on the new top-left point
                self.__width = self.__width + (self.__position[0] - point[0])
                self.__height = self.__height + (self.__position[1] - point[1])
                self.__position = point
            case "tr": # top-right
                # deduce new width and height based on the new top-right point
                self.__width = point[0] - self.__position[0]
                self.__height = self.__height + (self.__position[1] - point[1])
                self.__position = (self.__position[0], point[1])
            case "br": # bottom-right
                # deduce new width and height based on the new bottom-right point
                self.__width = point[0] - self.__position[0]
                self.__height = point[1] - self.__position[1]
                # do not need to change the position of the top left point
            case "bl": # bottom-left
                # deduce new width and height based on the new bottom-left point
                self.__width = self.__width + (self.__position[0] - point[0])
                self.__height = point[1] - self.__position[1]
                self.__position = (point[0], self.__position[1])

        # update the new vertices based on the new position, width and height, should be in order top left, top right, bottom right, bottom left
        self.__vertices = [
            (self.__position[0], self.__position[1]),
            (self.__position[0] + self.__width, self.__position[1]),
            (self.__position[0] + self.__width, self.__position[1] + self.__height),
            (self.__position[0], self.__position[1] + self.__height)
        ]
        self.set_vertices(self.__vertices)