import math

import numpy as np

from core.ray import Ray

from .Base import LightSource

# how spaced apart should the rays be
RAY_ANGLE_INCREMENT_DEGREES = 10.0


class PointSource(LightSource):
    def __init__(
        self,
        position,
        wavelength=550,
        intensity=1.0,
        angle_increment_degrees=RAY_ANGLE_INCREMENT_DEGREES,
    ):
        super().__init__(position, wavelength, intensity)
        self.update_angle_increment_degrees(angle_increment_degrees)

    def update_angle_increment_degrees(self, angle_increment_degrees):
        if not 0 < angle_increment_degrees <= 360:
            raise ValueError("angle_increment_degrees must be between 0 and 360")
        # find the number of rays
        ray_count = math.ceil(360 / angle_increment_degrees)
        # loop through for each ray
        for ray_index in range(ray_count):
            # calculate the angle that they make
            angle = math.radians(ray_index * angle_increment_degrees)
            # calculate the direction vector
            direction = np.array([math.cos(angle), math.sin(angle)])
            # create a new instance of a ray object
            self._LightSource__rays.append(
                Ray(
                self._LightSource__position,
                direction,
                self._LightSource__wavelength,
                self._LightSource__intensity,
            )
        )