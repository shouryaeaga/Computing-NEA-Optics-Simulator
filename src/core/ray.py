
class Ray:
    def __init__(self, start_point, direction, wavelength=550, intensity = 1.0, depth=0):
        self.start_point = start_point
        self.direction = direction
        self.wavelength = wavelength
        self.intensity = intensity
        self.depth = depth