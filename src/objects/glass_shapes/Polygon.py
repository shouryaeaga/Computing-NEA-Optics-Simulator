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
        self.__edges = []
        self.calculate_edges()

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

    def calculate_edges(self):
        edges = []
        num_vertices = len(self.__vertices)
        for i in range(num_vertices):
            # create an edge from the current vertex to the next vertex, befor ewrapping back to the first vertex
            start_vertex = self.__vertices[i]
            end_vertex = self.__vertices[(i + 1) % num_vertices]  # Wrap around to the first vertex
            edges.append((start_vertex, end_vertex))
        self.__edges = edges

    def get_edges(self):
        return self.__edges