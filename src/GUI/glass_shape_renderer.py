import pygame

from objects.glass_shapes.Polygon import Polygon


class GlassShapeRenderer:
    POLYGON_COLOUR = (185, 240, 255)
    POLYGON_ALPHA = 100
    SELECTED_SQUARE_COLOUR = (0, 255, 0)
    UNSELECTED_SQUARE_COLOUR = (255, 0, 0)
    SQUARE_POINT_SIZE = 5

    def __init__(self, screen: pygame.Surface):
        self.screen = screen

    def render(self, glass_shapes: list[object]):
        for glass_shape in glass_shapes:
            if isinstance(glass_shape, Polygon):
                self.render_polygon(glass_shape)
                self.render_selectable_points(glass_shape)

    def render_polygon(self, polygon: Polygon):
        vertices = polygon.get_vertices()
        min_x = min(vertex[0] for vertex in vertices)
        min_y = min(vertex[1] for vertex in vertices)
        max_x = max(vertex[0] for vertex in vertices)
        max_y = max(vertex[1] for vertex in vertices)

        polygon_surface = pygame.Surface(
            (max_x - min_x, max_y - min_y),
            pygame.SRCALPHA,
        )
        shifted_vertices = [
            (vertex[0] - min_x, vertex[1] - min_y)
            for vertex in vertices
        ]
        colour = self.POLYGON_COLOUR + (self.POLYGON_ALPHA,)
        pygame.draw.polygon(polygon_surface, colour, shifted_vertices)
        self.screen.blit(polygon_surface, (min_x, min_y))

    def render_selectable_points(self, polygon: Polygon):
        colour = (self.SELECTED_SQUARE_COLOUR 
                  if polygon.being_selected else self.UNSELECTED_SQUARE_COLOUR) 
        for vertex in polygon.get_vertices():
            self.render_point_square(vertex, colour)
            
    def render_point_square(self, position, colour):
        half_size = self.SQUARE_POINT_SIZE // 2
        pygame.draw.rect(
            self.screen,
            colour,
            (
                position[0] - half_size,
                position[1] - half_size,
                self.SQUARE_POINT_SIZE,
                self.SQUARE_POINT_SIZE,
            ),
        )
