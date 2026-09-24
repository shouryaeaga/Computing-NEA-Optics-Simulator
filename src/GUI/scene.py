from objects.light_sources.Base import LightSource


class Scene:
    def __init__(self):
        # double underscore indicates private attribute
        self.__light_sources: LightSource = []  # List to hold all light sources in the scene

    def add_light_source(self, light_source):
        self.__light_sources.append(light_source)  # Add a light source to the scene

    def get_light_sources(self):
        return self.__light_sources # getter method