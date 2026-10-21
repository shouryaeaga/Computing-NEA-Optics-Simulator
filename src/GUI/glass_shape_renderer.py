import pygame

from objects.glass_shapes.Polygon import Polygon


class GlassShapeRenderer:
    POLYGON_COLOUR = (185, 240, 255)
    POLYGON_ALPHA = 100
    SELECTED_SQUARE_COLOUR = (0, 255, 0)
    UNSELECTED_SQUARE_COLOUR = (255, 0, 0)
    SQUARE_POINT_SIZE = 5

    def __init__(self, screen: pygame.Surface, transparent_surface: pygame.Surface):
        self.__screen = screen
        self.__transparent_surface = transparent_surface

    def render(self, glass_shapes: list[object]):
        for glass_shape in glass_shapes:
            if isinstance(glass_shape, Polygon):
                self.render_polygon(glass_shape)
                self.render_selectable_points(glass_shape)

    def render_polygon(self, polygon: Polygon):
        vertices = polygon.get_vertices()
                
        colour = self.POLYGON_COLOUR + (self.POLYGON_ALPHA,)
        pygame.draw.polygon(self.__transparent_surface, colour, vertices)

    def render_selectable_points(self, polygon: Polygon):
        colour = (self.SELECTED_SQUARE_COLOUR 
                  if polygon.being_selected else self.UNSELECTED_SQUARE_COLOUR) 
        for vertex in polygon.get_vertices():
            self.render_point_square(vertex, colour)
            
    def render_point_square(self, position, colour):
        half_size = self.SQUARE_POINT_SIZE // 2
        pygame.draw.rect(
            self.__screen,
            colour,
            (
                position[0] - half_size,
                position[1] - half_size,
                self.SQUARE_POINT_SIZE,
                self.SQUARE_POINT_SIZE,
            ),
        )
