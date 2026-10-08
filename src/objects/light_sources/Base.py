class LightSource:
    # defines the shared behaviour for all light sources
    def __init__(self, position: tuple[float, float], wavelength: float = 550.0, intensity: float = 1.0, white_light: bool = False):
        # each light source requires a 2D position vector 
        self.__position = position
        # wavelength is required in nanometres
        self.__wavelength = wavelength
        # intensity is required so the user can configure how bright the source is
        self.__intensity = intensity
        # this is a boolean to configure whether the light source is emitting white light or monochromatic light
        self.__white_light = white_light

        self.__rays = []  # Initialize the rays list to store emitted rays
        self.being_selected = False

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

    def get_selectable_points(self):
        # Return a list of points that can be selected for this light source
        return [self.__position]

    def update_position(self, new_position: tuple[float, float]):
        # Update the position of the light source
        self.__position = new_position
        # Update the position of all emitted rays based on the new position
        for ray in self.__rays:
            ray.position = new_position