from objects.light_sources.Base import LightSource
from core.ray import Ray

class Scene:
    def __init__(self):
        # double underscore indicates private attribute
        self.__light_sources: list[LightSource] = []  # List to hold all light sources in the scene
        self.__glass_shapes: list[object] = []  # List to hold all glass shapes in the scene
        self.__refracted_light_rays: list[Ray] = []  # List to hold all refracted light rays in the scene

    def add_light_source(self, light_source: LightSource):
        self.__light_sources.append(light_source)  # Add a light source to the scene

    def get_light_sources(self):
        return self.__light_sources # getter method

    def add_glass_shape(self, glass_shape: object):
        self.__glass_shapes.append(glass_shape)  # Add a glass shape to the scene

    def get_glass_shapes(self):
        return self.__glass_shapes  # getter method

    def handle_refractions(self):
        # handle all intersections with light rays and glass shapes in the scene
        for light_source in self.__light_sources:
            for ray in light_source.get_emitted_rays():
                for glass_shape in self.__glass_shapes:
                    self.handle_intersection(ray, glass_shape)

    def handle_intersection(ray: Ray, glass_shape: object):
        # check whether the light ray intersects with the glass shape
        pass