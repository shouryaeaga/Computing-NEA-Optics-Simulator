# Defines the Ray class, to represent a light ray
class Ray:
    # Constructor for the Ray class, to store important data about each light ray.
    def __init__(
        self, start_point, direction, wavelength=550, intensity=1.0, depth=0,
        refractive_index=1.0, distance = 10000
    ):
        # start point is required to be a 2D vector for the position of the vector
        self.__start_point = start_point
        # this is the direction vector, which is required as a vector must have a start
        # point and direction of propogation
        self.__direction = direction
        # wavelength is required in nanometres
        self.__wavelength = wavelength
        # intensity of the light ray
        self.__intensity = intensity
        # this is recursion depth, to limit number of reflections and refractions
        # which can improve performance
        self.__depth = depth
        # 1.0 represents the surrounding air/vacuum medium.
        self.__refractive_index = refractive_index
        # the maximum distance the ray can travel
        self.__distance = distance

    def get_start_point(self):
        return self.__start_point

    def set_start_point(self, start_point):
        self.__start_point = start_point

    def get_direction(self):
        return self.__direction

    def set_direction(self, direction):
        self.__direction = direction

    def get_wavelength(self):
        return self.__wavelength

    def get_intensity(self):
        return self.__intensity

    def get_depth(self):
        return self.__depth

    def get_refractive_index(self):
        return self.__refractive_index

    def set_refractive_index(self, refractive_index):
        self.__refractive_index = refractive_index

    def set_distance(self, distance):
        self.__distance = distance

    def get_distance(self):
        return self.__distance