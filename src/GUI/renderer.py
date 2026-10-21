import pygame

from GUI.glass_shape_renderer import GlassShapeRenderer
from GUI.input_handler import InputHandler
from GUI.scene import Scene
from GUI.light_source_renderer import LightSourceRenderer
from objects.glass_shapes.Rectangle import Rectangle
from objects.light_sources.Beam import Beam
from objects.light_sources.PointSource import PointSource


class Renderer:
    WINDOW_SIZE = (800, 600)
    BACKGROUND_COLOUR = (34, 34, 34)
    # use a super sampling factor for the light rays to get rid of Moire patterns
    SUPER_SAMPLING_FACTOR = 4

    def __init__(self):
        pygame.init()
        self.__screen = pygame.display.set_mode(
            self.WINDOW_SIZE,
        )
        self.__transparent_surface = pygame.Surface(self.WINDOW_SIZE, pygame.SRCALPHA)
        self.__transparent_surface.fill((0, 0, 0, 0))  # Fill with transparent color

        self.__transparent_ray_surface = pygame.Surface(
            (self.WINDOW_SIZE[0] * self.SUPER_SAMPLING_FACTOR, self.WINDOW_SIZE[1] * self.SUPER_SAMPLING_FACTOR),
            pygame.SRCALPHA
        )
        pygame.display.set_caption("Optics Simulator")
        self.clock = pygame.time.Clock()

        self.scene = Scene()
        self.input_handler = InputHandler(self.scene)
        self.light_source_renderer = LightSourceRenderer(self.__screen, self.__transparent_ray_surface)
        self.glass_shape_renderer = GlassShapeRenderer(self.__screen, self.__transparent_surface)

        test_glass_shape = Rectangle(100, 50, (400, 400), 1.5)
        self.scene.add_glass_shape(test_glass_shape)
        test_beam = Beam(point_one=(100, 100), point_two=(200, 100), ray_spacing=5, intensity=0.75)
        self.scene.add_light_source(test_beam)
        test_point_source = PointSource(position=(600, 100), intensity=0.75)
        self.scene.add_light_source(test_point_source)
        

    def run(self):
        while True:
            self.handle_events()
            self.render()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            self.input_handler.handle_event(event)

        self.input_handler.update(pygame.mouse.get_pos())

    def render(self):
        self.__screen.fill(self.BACKGROUND_COLOUR)
        self.__transparent_surface.fill((0, 0, 0, 0))  # Clear the transparent surface
        self.light_source_renderer.clear_rays()
        # need to render the glass shapes before the light rays so that the rays appear on top of the glass shapes
        self.glass_shape_renderer.render(
            self.scene.get_glass_shapes()
        )
        self.light_source_renderer.render(
            self.scene.get_light_sources()
        )
        
        self.__screen.blit(self.__transparent_surface, (0, 0))
        self.__screen.blit(pygame.transform.smoothscale(self.__transparent_ray_surface, self.WINDOW_SIZE), (0, 0))
        pygame.display.flip()
