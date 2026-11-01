import pygame

from GUI.glass_shape_renderer import GlassShapeRenderer
from GUI.input_handler import InputHandler
from GUI.scene import Scene
from GUI.light_source_renderer import LightSourceRenderer
from objects.glass_shapes.Rectangle import Rectangle
from objects.light_sources.Beam import Beam
from objects.light_sources.PointSource import PointSource


class Renderer:
    __WINDOW_SIZE = (800, 600)
    __BACKGROUND_COLOUR = (34, 34, 34)
    # use a super sampling factor for the light rays to get rid of Moire patterns
    __SUPER_SAMPLING_FACTOR = 4

    def __init__(self):
        pygame.init()
        self.__screen = pygame.display.set_mode(
            self.__WINDOW_SIZE,
        )
        self.__transparent_surface = pygame.Surface(self.__WINDOW_SIZE, pygame.SRCALPHA)
        self.__transparent_surface.fill((0, 0, 0, 0))  # Fill with transparent color

        self.__transparent_ray_surface = pygame.Surface(
            (self.__WINDOW_SIZE[0] * self.__SUPER_SAMPLING_FACTOR, self.__WINDOW_SIZE[1] * self.__SUPER_SAMPLING_FACTOR),
            pygame.SRCALPHA
        )
        pygame.display.set_caption("Optics Simulator")
        self.__clock = pygame.time.Clock()

        self.__scene = Scene()
        self.__input_handler = InputHandler(self.__scene)
        self.__light_source_renderer = LightSourceRenderer(self.__screen, self.__transparent_ray_surface)
        self.__glass_shape_renderer = GlassShapeRenderer(self.__screen, self.__transparent_surface)

        test_glass_shape = Rectangle(100, 50, (400, 400), 1.5)
        self.__scene.add_glass_shape(test_glass_shape)
        test_beam = Beam(point_one=(100, 100), point_two=(200, 100), ray_spacing=5, intensity=0.75)
        self.__scene.add_light_source(test_beam)
        test_point_source = PointSource(position=(600, 100), intensity=0.75)
        self.__scene.add_light_source(test_point_source)
        

    def run(self):
        while True:
            self.__handle_events()
            self.__render()
            self.__clock.tick(60)

    def __handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            self.__input_handler.handle_event(event)

        self.__input_handler.update(pygame.mouse.get_pos())

    def __render(self):
        self.__screen.fill(self.__BACKGROUND_COLOUR)
        self.__transparent_surface.fill((0, 0, 0, 0))  # Clear the transparent surface
        self.__light_source_renderer.clear_rays()
        # need to render the glass shapes before the light rays so that the rays appear on top of the glass shapes
        self.__glass_shape_renderer.render(
            self.__scene.get_glass_shapes()
        )
        self.__light_source_renderer.render(
            self.__scene.get_light_sources()
        )
        
        self.__screen.blit(self.__transparent_surface, (0, 0))
        self.__screen.blit(pygame.transform.smoothscale(self.__transparent_ray_surface, self.__WINDOW_SIZE), (0, 0))
        pygame.display.flip()
