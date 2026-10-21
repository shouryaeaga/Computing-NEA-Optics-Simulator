import pygame

from core.ray import Ray
from objects.light_sources.Base import LightSource
from objects.light_sources.Beam import Beam
from objects.light_sources.PointSource import PointSource
from objects.light_sources.SingleRay import SingleRay


class LightSourceRenderer:
    LIGHT_SOURCE_COLOUR = (255, 245, 182)
    LIGHT_RAY_COLOUR = (255, 245, 182)
    SELECTED_SQUARE_COLOUR = (0, 255, 0)
    UNSELECTED_SQUARE_COLOUR = (255, 0, 0)
    SQUARE_POINT_SIZE = 5

    def __init__(self, screen: pygame.Surface, transparent_surface: pygame.Surface, super_sampling_factor: int = 4):
        if super_sampling_factor <= 0:
            raise ValueError("super_sampling_factor must be greater than zero.")

        self.__screen = screen
        self.__transparent_surface = transparent_surface
        self.__super_sampling_factor = super_sampling_factor

    def clear_rays(self):
        # Keep the RGB colour in transparent pixels so smoothscale does not
        # introduce dark fringes when it interpolates the ray edges.
        self.__transparent_surface.fill(self.LIGHT_RAY_COLOUR + (0,))

    def render(self, light_sources: list[LightSource]):
        for light_source in light_sources:
            self.render_rays(light_source)
            self.render_source(light_source)
            self.render_selectable_points(light_source)

    def render_rays(self, light_source: LightSource):
        for ray in light_source.get_emitted_rays():
            self.render_ray(ray)

    def render_ray(self, ray: Ray):
        line_length = 1000
        end_point = ray.start_point + line_length * ray.direction
        pygame.draw.line(
            self.__transparent_surface,
            self.LIGHT_RAY_COLOUR + (int(255*ray.intensity),),
            tuple(point * self.__super_sampling_factor for point in ray.start_point),
            tuple(point * self.__super_sampling_factor for point in end_point),
            int(self.__super_sampling_factor * 1.5)
        )

    def render_source(self, light_source: LightSource):
        if isinstance(light_source, PointSource):
            pygame.draw.circle(
                self.__screen,
                self.LIGHT_SOURCE_COLOUR,
                light_source.get_position(),
                light_source.point_source_radius,
            )
        elif isinstance(light_source, Beam):
            point_one, point_two = light_source.get_endpoints()
            pygame.draw.aaline(
                self.__screen,
                self.LIGHT_SOURCE_COLOUR,
                point_one,
                point_two,
            )

    def render_selectable_points(self, light_source: LightSource):
        if isinstance(light_source, Beam):
            points = light_source.get_endpoints()
        elif isinstance(light_source, SingleRay):
            points = light_source.get_selectable_points()
        elif isinstance(light_source, PointSource):
            points = [light_source.get_position()]
        else:
            points = []

        colour = (
            self.SELECTED_SQUARE_COLOUR
            if light_source.being_selected
            else self.UNSELECTED_SQUARE_COLOUR
        )

        for point in points:
            self.render_point_square(point, colour)

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
