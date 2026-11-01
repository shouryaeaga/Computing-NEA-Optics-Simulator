import pygame

from objects.glass_shapes.Polygon import Polygon


class GlassShapeRenderer:
    __POLYGON_COLOUR = (185, 240, 255)
    __POLYGON_ALPHA = 100
    __SELECTED_SQUARE_COLOUR = (0, 255, 0)
    __UNSELECTED_SQUARE_COLOUR = (255, 0, 0)
    __SQUARE_POINT_SIZE = 5

    def __init__(self, screen: pygame.Surface, transparent_surface: pygame.Surface):
        self.__screen = screen
        self.__transparent_surface = transparent_surface

    def render(self, glass_shapes: list[object]):
        for glass_shape in glass_shapes:
            if isinstance(glass_shape, Polygon):
                self.__render_polygon(glass_shape)
                self.__render_selectable_points(glass_shape)

    def __render_polygon(self, polygon: Polygon):
        vertices = polygon.get_vertices()
                
        colour = self.__POLYGON_COLOUR + (self.__POLYGON_ALPHA,)
        pygame.draw.polygon(self.__transparent_surface, colour, vertices)

    def __render_selectable_points(self, polygon: Polygon):
        colour = (self.__SELECTED_SQUARE_COLOUR
                  if polygon.is_selected() else self.__UNSELECTED_SQUARE_COLOUR)
        for vertex in polygon.get_vertices():
            self.__render_point_square(vertex, colour)
            
    def __render_point_square(self, position, colour):
        half_size = self.__SQUARE_POINT_SIZE // 2
        pygame.draw.rect(
            self.__screen,
            colour,
            (
                position[0] - half_size,
                position[1] - half_size,
                self.__SQUARE_POINT_SIZE,
                self.__SQUARE_POINT_SIZE,
            ),
        )
