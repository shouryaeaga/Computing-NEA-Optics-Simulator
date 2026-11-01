class Polygon:
    def __init__(self, 
                 vertices: list[tuple[int, int]], 
                 position: tuple[int, int],
                 refractive_index: float,
                 ):
        self.__vertices = vertices
        self.__position = position
        self.__refractive_index = refractive_index
        self.__being_selected = False

    def get_vertices(self):
        return self.__vertices

    def get_position(self):
        return self.__position

    def get_refractive_index(self):
        return self.__refractive_index

    def is_selected(self):
        return self.__being_selected

    def set_selected(self, selected: bool):
        self.__being_selected = selected