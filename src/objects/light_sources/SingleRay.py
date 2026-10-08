from core.ray import Ray

from .Base import LightSource
import numpy as np

class SingleRay (LightSource):
    def __init__(self, position: tuple[float, float], direction_point: tuple[float, float], wavelength: float = 550.0, intensity: float = 1.0, point_source_radius=3.0):
        super().__init__(position, wavelength, intensity)
        self.point_source_radius = point_source_radius

        self.__direction_point = direction_point

        self.__ray_direction = np.subtract(
            self.__direction_point, self._LightSource__position
        ).astype(float)
        # normalise the direction vector, so that it is a unit length
        # this fixes the bug, as previously, it would add a direction vector that was very long
        direction_length = np.linalg.norm(self.__ray_direction)
        self.__ray_direction /= direction_length

        # Start the ray point_source_radius units away from the source.
        position = self._LightSource__position + (self.__ray_direction * self.point_source_radius)
        ray = Ray(
            position,
            self.__ray_direction,
            self._LightSource__wavelength,
            self._LightSource__intensity,
        )
        # Add the emitted ray to the rays list of the light source
        self._LightSource__rays.append(ray)
        

    def update_direction(self, new_direction_point):
        # Update the direction point and recalculate the direction vector
        self.__direction_point = new_direction_point
        self.__ray_direction = np.subtract(
            self.__direction_point, self._LightSource__position
        ).astype(float)
        direction_length = np.linalg.norm(self.__ray_direction)
        self.__ray_direction /= direction_length
        # normalise the direction vector, so that it is a unit length
        # this fixes the bug, as previously, it would add a direction vector that was very long
        # Start the ray point_source_radius units away from the source.
        position = self._LightSource__position + (self.__ray_direction * self.point_source_radius)

        # Update the existing ray's position and direction
        # Update the existing ray's direction
        if self._LightSource__rays:
            self._LightSource__rays[0].position = position
            self._LightSource__rays[0].direction = self.__ray_direction

    def get_selectable_points(self):
        # Return a list of points that can be selected for this light source
        return [self.get_position(), self.__direction_point]