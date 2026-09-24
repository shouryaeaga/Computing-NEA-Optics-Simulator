import math

import numpy as np

from core.ray import Ray

from .Base import LightSource


class Beam(LightSource):
    # Represents a beam of parallel light rays

    def __init__(
        self,
        point_one,
        point_two,
        ray_spacing,
        wavelength=550,
        intensity=1.0,
    ):
        # Use the first beam point as the light source position
        super().__init__(point_one, wavelength, intensity)

        # Store the two points connected by the beam
        self.__point_one = np.array(point_one)
        self.__point_two = np.array(point_two)

        # Store the spacing between adjacent rays
        self.__ray_spacing = ray_spacing

        # Check that the two points are different
        if np.array_equal(self.__point_one, self.__point_two):
            raise ValueError("The beam points must be different.")

        # Check that the ray spacing is positive
        if ray_spacing <= 0:
            raise ValueError("ray_spacing must be greater than zero.")

        # Calculate the direction normal to the beam
        self.__direction = self.calculate_normal_direction()

        # Create the rays emitted by the beam
        self.create_rays()

    def calculate_normal_direction(self):
        # Calculate the vector joining the two beam points
        connecting_vector = self.__point_two - self.__point_one

        # Create a perpendicular vector
        return np.array(
            [
                -connecting_vector[1],
                connecting_vector[0],
            ]
        )

    def create_rays(self):
        # Calculate the vector joining the two beam points
        connecting_vector = self.__point_two - self.__point_one

        # Calculate the length of the beam
        beam_length = np.linalg.norm(connecting_vector)

        # Normalise the connecting vector
        unit_vector = connecting_vector / beam_length

        # Calculate the number of rays that fit along the beam
        ray_count = math.floor(beam_length / self.__ray_spacing) + 1

        # Create a ray at each required spacing
        for ray_index in range(ray_count):
            # Calculate the ray's starting position
            ray_position = (
                self.__point_one
                + unit_vector * ray_index * self.__ray_spacing
            )

            # Create the ray travelling normal to the beam
            ray = Ray(
                ray_position,
                self.__direction,
                self._LightSource__wavelength,
                self._LightSource__intensity,
            )

            # Add the ray to the inherited light source ray list
            self._LightSource__rays.append(ray)