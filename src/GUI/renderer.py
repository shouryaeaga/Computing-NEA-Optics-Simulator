from GUI.scene import Scene
from core.ray import Ray
from objects.light_sources.Base import LightSource
from objects.light_sources.PointSource import PointSource
import pygame

class Renderer:
    def __init__(self):
        # Initialize the Pygame library
        pygame.init()
        # Set up the display window with a specific size
        self.__screen = pygame.display.set_mode((800, 600))
        # Set the title of the window
        pygame.display.set_caption("Optics Simulator")
        self.__clock = pygame.time.Clock()
        # Define a background color (black in this case)
        self.__background_color = (0, 0, 0)
        self.__scene = Scene()  # Initialize a Scene object to manage light sources and rays
        self.__LIGHT_SOURCE_COLOUR = (255, 220, 70)
        self.__LIGHT_SOURCE_RADIUS = 3
        self.__LIGHT_RAY_COLOUR_TEMPORARY = (80, 220, 255)

        test_light_source = PointSource((400, 400))

        self.__scene.add_light_source(test_light_source)

        while True:
            self.render_scene()  # Continuously render the scene in a loop

    def render_scene(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

        # Iterate through all light sources in the scene and emit rays
        self.__screen.fill(self.__background_color)  # Clear the screen with the background color

        # call subroutine to handle light sources
        self.render_light_sources()
        
        pygame.display.flip()
        self.__clock.tick(60)
        
    def render_light_sources(self):
        light_sources: list[LightSource] = self.__scene.get_light_sources()

        for light_source in light_sources:
            # draw a circle where position of light source is
            pygame.draw.circle(self.__screen, self.__LIGHT_SOURCE_COLOUR, (light_source.get_position()), self.__LIGHT_SOURCE_RADIUS)
            rays = light_source.get_emitted_rays()
            for ray in rays:
                self.render_light_ray(ray)

    def render_light_ray(self, light_ray: Ray):
        # implementation for rendering an invidividual light ray
        # create a pygame line
        LAMBDA_END = 1000 # temporary value for drawing infinite lines without any objects
        pygame.draw.line(self.__screen, self.__LIGHT_RAY_COLOUR_TEMPORARY, light_ray.start_point, light_ray.start_point + LAMBDA_END*light_ray.direction)
        
