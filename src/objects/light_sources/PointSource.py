from .Base import LightSource

class PointSource (LightSource):
    def __init__(self, position, wavelength=550, intensity=1.0, direction_point=None):
        super().__init__(position, wavelength, intensity)
        self.direction_point = direction_point

    def emit_ray(self):
        # Implementation for emitting a ray from the point source
        pass
