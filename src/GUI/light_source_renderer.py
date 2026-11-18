import pygame
import numpy as np

from core.ray import Ray
from objects.light_sources.Base import LightSource
from objects.light_sources.Beam import Beam
from objects.light_sources.PointSource import PointSource
from objects.light_sources.SingleRay import SingleRay
from GUI.scene import Scene


class LightSourceRenderer:
    __LIGHT_SOURCE_COLOUR = (255, 245, 182)
    __LIGHT_RAY_COLOUR = (255, 245, 182)
    __SELECTED_SQUARE_COLOUR = (0, 255, 0)
    __UNSELECTED_SQUARE_COLOUR = (255, 0, 0)
    __SQUARE_POINT_SIZE = 5

    def __init__(self, screen: pygame.Surface, transparent_surface: pygame.Surface, scene: Scene, super_sampling_factor: int = 4):
        if super_sampling_factor <= 0:
            raise ValueError("super_sampling_factor must be greater than zero.")

        self.__screen = screen
        self.__transparent_surface = transparent_surface
        self.__super_sampling_factor = super_sampling_factor
        self.__scene = scene
        self.__ray_mask = pygame.Surface(
            (self.__transparent_surface.get_width(),
             self.__transparent_surface.get_height()),
            0,
            8
        )
        self.__ray_colour_mask = pygame.Surface(
            (self.__transparent_surface.get_width(),
             self.__transparent_surface.get_height())
        )

    def clear_rays(self):
        # Keep the RGB colour in transparent pixels so smoothscale does not
        # introduce dark fringes when it interpolates the ray edges.
        self.__transparent_surface.fill(self.__LIGHT_RAY_COLOUR + (0,))
        self.__ray_mask.fill(0)
        self.__ray_colour_mask.fill(self.__LIGHT_RAY_COLOUR)

    def render(self, light_sources: list[LightSource], light_rays: list[Ray], scene_changed: bool = False):
        for light_source in light_sources:
            self.__render_source(light_source)
            self.__render_selectable_points(light_source)

        if scene_changed:
            self.clear_rays()
            # Draw weaker rays first, so more intense rays are drawn on top.
            for ray in sorted(light_rays, key=lambda item: item.get_intensity()):
                self.__render_ray(ray)
            self.__apply_ray_alpha()

    def wavelength_to_rgb(self, wavelength: float) -> tuple[int, int, int]:
        if wavelength < 380 or wavelength > 780:
            raise ValueError("Wavelength must be between 380 and 750 nm.")

        # use a simple piecewise function which can convert wavelengths to RGB values
        # algorithm found online
        if 380 <= wavelength < 440: r,g,b = (440-wavelength) / (440 - 380), 0.0, 1.0
        elif 440 <= wavelength < 490: r,g,b = 0.0, (wavelength - 440) / 50, 1.0
        elif 490 <= wavelength < 510: r,g,b = 0.0, 1.0, (510 - wavelength) / 20
        elif 510 <= wavelength < 580: r,g,b = (wavelength - 510) / 70, 1.0, 0.0
        elif 580 <= wavelength < 645: r,g,b = 1.0, (645 - wavelength) / 65, 0.0
        elif 645 <= wavelength <= 780: r,g,b = 1.0, 0.0, 0.0

        if 380 <= wavelength < 420: factor = 0.3 + 0.7 * (wavelength - 380) / 40
        elif 420 <= wavelength < 700: factor = 1.0
        elif 700 <= wavelength <= 780: factor = 0.3 + 0.7 * (780 - wavelength) / 80

        gamma = 0.8
        r = (r * factor) ** gamma
        g = (g * factor) ** gamma
        b = (b * factor) ** gamma
        return int(r * 255), int(g * 255), int(b * 255)

    def __render_ray(self, ray: Ray):
        line_length = ray.get_distance()
        end_point = ray.get_start_point() + line_length * ray.get_direction()
        colour = self.wavelength_to_rgb(ray.get_wavelength())
        pygame.draw.line(
            self.__ray_mask,
            # this intensity is used to set the alpha channel of the ray, so it must be between 0 and 255
            int(np.clip(255 * ray.get_intensity(), 0, 255)),
            tuple(point * self.__super_sampling_factor for point in ray.get_start_point()),
            tuple(point * self.__super_sampling_factor for point in end_point),
            int(self.__super_sampling_factor * 1.5)
        )
        pygame.draw.line(
            self.__ray_colour_mask,
            colour,
            tuple(point * self.__super_sampling_factor for point in ray.get_start_point()),
            tuple(point * self.__super_sampling_factor for point in end_point),
            int(self.__super_sampling_factor * 1.5)
        )

    def __apply_ray_alpha(self):
        # Apply the maximum ray intensity as alpha and its wavelength colour as RGB.
        intensity_mask = pygame.surfarray.pixels2d(self.__ray_mask)
        destination_alpha = pygame.surfarray.pixels_alpha(self.__transparent_surface)
        destination_alpha[:] = intensity_mask
        destination_rgb = pygame.surfarray.pixels3d(self.__transparent_surface)
        source_rgb = pygame.surfarray.pixels3d(self.__ray_colour_mask)
        destination_rgb[:] = source_rgb

    def __render_source(self, light_source: LightSource):
        if isinstance(light_source, PointSource):
            pygame.draw.circle(
                self.__screen,
                self.__LIGHT_SOURCE_COLOUR,
                light_source.get_position(),
                light_source.get_point_source_radius(),
            )
        elif isinstance(light_source, Beam):
            point_one, point_two = light_source.get_endpoints()
            pygame.draw.aaline(
                self.__screen,
                self.__LIGHT_SOURCE_COLOUR,
                point_one,
                point_two,
            )

    def __render_selectable_points(self, light_source: LightSource):
        if isinstance(light_source, Beam):
            points = light_source.get_endpoints()
        elif isinstance(light_source, SingleRay):
            points = light_source.get_selectable_points()
        elif isinstance(light_source, PointSource):
            points = [light_source.get_position()]
        else:
            points = []

        colour = (
            self.__SELECTED_SQUARE_COLOUR
            if light_source.is_selected()
            else self.__UNSELECTED_SQUARE_COLOUR
        )

        for point in points:
            self.__render_point_square(point, colour)

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
