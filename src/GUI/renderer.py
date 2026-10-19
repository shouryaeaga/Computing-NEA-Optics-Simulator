import pygame

from GUI.glass_shape_renderer import GlassShapeRenderer
from GUI.input_handler import InputHandler
from GUI.scene import Scene
from GUI.light_source_renderer import LightSourceRenderer
from objects.glass_shapes.Rectangle import Rectangle


class Renderer:
    WINDOW_SIZE = (800, 600)
    BACKGROUND_COLOUR = (34, 34, 34)

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            self.WINDOW_SIZE,
            pygame.RESIZABLE,
        )
        pygame.display.set_caption("Optics Simulator")
        self.clock = pygame.time.Clock()

        self.scene = Scene()
        self.input_handler = InputHandler(self.scene)
        self.light_source_renderer = LightSourceRenderer(self.screen)
        self.glass_shape_renderer = GlassShapeRenderer(self.screen)

        test_glass_shape = Rectangle(100, 50, (400, 400), 1.5)
        self.scene.add_glass_shape(test_glass_shape)

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
        self.screen.fill(self.BACKGROUND_COLOUR)
        self.light_source_renderer.render(
            self.scene.get_light_sources()
        )
        self.glass_shape_renderer.render(
            self.scene.get_glass_shapes()
        )
        pygame.display.flip()
