class LightSource:
    # defines the shared behaviour for all light sources
    def __init__(self, position, wavelength=550, intensity=1.0, white_light=False):
        # each light source requires a 2D position vector 
        self.__position = position
        # wavelength is required in nanometres
        self.__wavelength = wavelength
        # intensity is required so the user can configure how bright the source is
        self.__intensity = intensity
        # this is a boolean to configure whether the light source is emitting white light or monochromatic light
        self.__white_light = white_light

        self.__rays = []  # Initialize the rays list to store emitted rays

    def get_emitted_rays(self):
        # Return the list of emitted rays
        return self.__rays

    def get_position(self):
        # return the position
        return self.__position

    def get_wavelength(self):
        return self.__wavelength

    def get_intensity(self):
        return self.__intensity

    def get_white_light(self):
        return self.__white_light