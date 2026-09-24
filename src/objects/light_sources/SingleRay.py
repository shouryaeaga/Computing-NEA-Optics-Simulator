from core.ray import Ray

from .Base import LightSource
import numpy as np

class SingleRay (LightSource):
    def __init__(self, position, direction_point, wavelength=550, intensity=1.0):
        super().__init__(position, wavelength, intensity)
        
        self.__direction_point = direction_point

        self.__ray_direction = np.subtract(
            self.__direction_point, self._LightSource__position
        )  # Calculate the direction vector from numpy arrays
        # Now instantiate a Ray object with the calculated direction and other properties
        ray = Ray(
            self._LightSource__position,
            self.__ray_direction,
            self._LightSource__wavelength,
            self._LightSource__intensity,
        )
        # Add the emitted ray to the rays list of the light source
        self._LightSource__rays.append(ray)
        
    

    def update_direction(self, new_direction_point):
        # Update the direction point and recalculate the direction vector
        self.__direction_point = new_direction_point
        self.__ray_direction = np.subtract(self.__direction_point, self.__position)
        # Update the existing ray's direction
        if super().__rays:
            super().__rays[0].direction = self.__ray_direction
