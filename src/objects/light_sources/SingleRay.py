from core.ray import Ray

from .Base import LightSource
import numpy as np

class SingleRay (LightSource):
    def __init__(self, position: tuple[float, float], direction_point: tuple[float, float], wavelength: float = 550.0, intensity: float = 1.0, point_source_radius=3.0):
        super().__init__(position, wavelength, intensity)
        self.__point_source_radius = point_source_radius

        self.__direction_point = direction_point

        self.__ray_direction = np.subtract(
            self.__direction_point, self.get_position()
        ).astype(float)
        # normalise the direction vector, so that it is a unit length
        # this fixes the bug, as previously, it would add a direction vector that was very long
        direction_length = np.linalg.norm(self.__ray_direction)
        self.__ray_direction /= direction_length

        # Start the ray point_source_radius units away from the source.
        position = self.get_position() + (self.__ray_direction * self.__point_source_radius)
        ray = Ray(
            position,
            self.__ray_direction,
            self.get_wavelength(),
            self.get_intensity(),
        )
        # Add the emitted ray to the rays list of the light source
        self.get_emitted_rays().append(ray)
        

    def update_direction(self, new_direction_point):
        # Update the direction point and recalculate the direction vector
        self.__direction_point = new_direction_point
        self.__ray_direction = np.subtract(
            self.__direction_point, self.get_position()
        ).astype(float)
        direction_length = np.linalg.norm(self.__ray_direction)
        self.__ray_direction /= direction_length
        # normalise the direction vector, so that it is a unit length
        # this fixes the bug, as previously, it would add a direction vector that was very long
        # Start the ray point_source_radius units away from the source.
        position = self.get_position() + (self.__ray_direction * self.__point_source_radius)

        # Update the existing ray's position and direction
        # Update the existing ray's direction
        if self.get_emitted_rays():
            self.get_emitted_rays()[0].set_start_point(position)
            self.get_emitted_rays()[0].set_direction(self.__ray_direction)

    def get_selectable_points(self):
        # Return a list of points that can be selected for this light source
        return [self.get_position(), self.__direction_point]