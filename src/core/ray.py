# Defines the Ray class, to represent a light ray
class Ray:
    # Constructor for the Ray class, to store important data about each light ray.
    def __init__(self, start_point, direction, wavelength=550, intensity = 1.0, depth=0):
        # start point is required to be a 2D vector for the position of the vector
        self.start_point = start_point
        # this is the direction vector, which is required as a vector must have a start
        # point and direction of propogation
        self.direction = direction
        # wavelength is required in nanometres
        self.wavelength = wavelength
        # intensity of the light ray
        self.intensity = intensity
        # this is recursion depth, to limit number of reflections and refractions
        # which can improve performance
        self.depth = depth
        