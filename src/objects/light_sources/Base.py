class LightSource:
    # defines the shared behaviour for all light sources
    def __init__(self, position, wavelength=550, intensity=1.0, white_light=False):
        self.position = position
        self.wavelength = wavelength
        self.intensity = intensity
        self.white_light = white_light

    def emit_ray(self):
        # this method should be implemented by subclasses to emit rays in a specific manner
        raise NotImplementedError("Subclasses must implement the emit_ray method.")