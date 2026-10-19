from GUI.scene import Scene
from core.ray import Ray
from objects.light_sources.Beam import Beam
from objects.light_sources.SingleRay import SingleRay
from objects.light_sources.Base import LightSource
from objects.light_sources.PointSource import PointSource
import pygame

class Renderer:
    def __init__(self):
        # Initialize the Pygame library
        pygame.init()
        # Set up the display window with a specific size
        self.__screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        # Set the title of the window
        pygame.display.set_caption("Optics Simulator")
        self.__clock = pygame.time.Clock()
        # Define a background color (very dark gray in this case)
        self.__background_color = (34, 34, 34)
        self.__scene = Scene()  # Initialize a Scene object to manage light sources and rays
        # make variables to hold dragging state
        self.__dragging = False
        self.__dragged_light_source = None
        self.__dragged_point_index = None
        # constants to define certain colours
        self.__LIGHT_SOURCE_COLOUR = (255, 245, 182)
        self.__LIGHT_SOURCE_RADIUS = 5
        self.__LIGHT_RAY_COLOUR = (255, 245, 182)
        self.__SQUARE_POINT_SIZE = 5
        self.__UNSELECTED_SQUARE_COLOUR = (255, 0, 0)
        self.__SELECTED_SQUARE_COLOUR = (0, 255, 0)

        # single ray
        test_light_source_1 = SingleRay((50, 50), (100, 100), point_source_radius=self.__LIGHT_SOURCE_RADIUS)

        # point source
        test_light_source_2 = PointSource((400, 300), point_source_radius=self.__LIGHT_SOURCE_RADIUS)

        #beam
        test_light_source_3 = Beam((300, 350), (350, 400), 5)

        self.__scene.add_light_source(test_light_source_1)
        self.__scene.add_light_source(test_light_source_2)
        self.__scene.add_light_source(test_light_source_3)

        while True:
            self.__render_scene()  # Continuously render the scene in a loop

    def __render_scene(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.__start_drag(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.__stop_drag()
            elif event.type == pygame.MOUSEMOTION and not self.__dragging:
                # get mouse input to update the location of light sources points
                self.__handle_mouse_hovers(event)

        if self.__dragging:
            self.__update_dragged_light_source(pygame.mouse.get_pos())
        # Iterate through all light sources in the scene and emit rays
        self.__screen.fill(self.__background_color)  # Clear the screen with the background color

        # call subroutine to handle light sources
        self.__render_light_sources()
        
        pygame.display.flip()
        self.__clock.tick(60)

    def __start_drag(self, mouse_position):
        # start looping through all the light sources in the scene, to check if the mouse is above them
        for light_source in self.__scene.get_light_sources():
            # loop through all the selectable points of the light source
            for point_index, point in enumerate(light_source.get_selectable_points()):
                # check if the selectable box is in range of the mouse
                if (
                    abs(mouse_position[0] - point[0]) < self.__SQUARE_POINT_SIZE
                    and abs(mouse_position[1] - point[1]) < self.__SQUARE_POINT_SIZE
                ):
                    # set it to be the dragged object
                    # the point index is used to determine which box is being selected
                    self.__dragging = True
                    self.__dragged_light_source = light_source
                    self.__dragged_point_index = point_index
                    light_source.being_selected = True
                    return

    def __stop_drag(self):
        # set back to default
        self.__dragging = False
        self.__dragged_light_source = None
        self.__dragged_point_index = None

    def __update_dragged_light_source(self, mouse_position):
        if self.__dragged_light_source is None:
            return

        if isinstance(self.__dragged_light_source, Beam):
            # Update the beam points based on the dragged point index
            endpoints = self.__dragged_light_source.get_endpoints()
            updated_endpoints = list(endpoints)
            updated_endpoints[self.__dragged_point_index] = mouse_position
            # automatically update the light source's position to be the end points
            # the star operator just unpacks the list automatically
            self.__dragged_light_source.update_points(*updated_endpoints)
        elif isinstance(self.__dragged_light_source, SingleRay) and self.__dragged_point_index == 1:
            # Update direction point if that is what we're dragging on
            self.__dragged_light_source.update_direction(mouse_position)
        elif isinstance(self.__dragged_light_source, SingleRay):
            # update the position if the dragged point index is 0 (the source point)
            self.__dragged_light_source.update_position(mouse_position)
            self.__dragged_light_source.update_direction(
                self.__dragged_light_source.get_selectable_points()[1]
            )
        else:
            # update the point source's position, because that is the only exposed endpoint
            # for the point source
            self.__dragged_light_source.update_position(mouse_position)

    def __handle_mouse_hovers(self, event):
        # check whether it is hovering over a light source point
        for light_source in self.__scene.get_light_sources():
            light_source.being_selected = any(
                abs(event.pos[0] - point[0]) < self.__SQUARE_POINT_SIZE
                and abs(event.pos[1] - point[1]) < self.__SQUARE_POINT_SIZE
                for point in light_source.get_selectable_points()
            )
        
    def __render_light_sources(self):
        light_sources: list[LightSource] = self.__scene.get_light_sources()

        for light_source in light_sources:
            for ray in light_source.get_emitted_rays():
                self.__render_light_ray(ray)
            # detect whether the light source is a point type source (SingleRay or PointSource) or if it is a beam source.
            if isinstance(light_source, PointSource):
                #Render as a point type source
                self.__render_point_source(light_source)
            elif isinstance(light_source, Beam):
                # render as a beam type source
                self.__render_beam_source(light_source)

            if isinstance(light_source, Beam):
                for endpoint in light_source.get_endpoints():
                    # draw a square at the location of the beam endpoints
                    self.__render_point_square(endpoint, colour=self.__SELECTED_SQUARE_COLOUR if light_source.being_selected else self.__UNSELECTED_SQUARE_COLOUR)
            elif isinstance(light_source, SingleRay):
                # draw a square at the location of the source
                for point in light_source.get_selectable_points():
                    self.__render_point_square(point, colour=self.__SELECTED_SQUARE_COLOUR if light_source.being_selected else self.__UNSELECTED_SQUARE_COLOUR)
            elif isinstance(light_source, PointSource):
                # draw a square at the location of the point source
                self.__render_point_square(light_source.get_position(), colour=self.__SELECTED_SQUARE_COLOUR if light_source.being_selected else self.__UNSELECTED_SQUARE_COLOUR)

            

    def __render_point_square(self, position, colour=None):
        # select the colour of the square based on whether it is selected or not
        if colour is None:
            colour = self.__UNSELECTED_SQUARE_COLOUR
        # draw a square, defined by its top left corner's x, y, then width and height in that order, which is the 3rd parameter
        pygame.draw.rect(
            self.__screen,
            colour,
            (
                position[0] - self.__SQUARE_POINT_SIZE // 2,
                position[1] - self.__SQUARE_POINT_SIZE // 2,
                self.__SQUARE_POINT_SIZE,
                self.__SQUARE_POINT_SIZE,
            ),
        )

    def __render_point_source(self, light_source):
        # draw a circle onto the screen with the correct colours
        pygame.draw.circle(
            self.__screen,
            self.__LIGHT_SOURCE_COLOUR,
            light_source.get_position(),
            light_source.point_source_radius
        )

    def __render_beam_source(self, light_source: Beam):
        # make a line for the beam light source
        point_one, point_two = light_source.get_endpoints()
        pygame.draw.aaline(self.__screen,
                         self.__LIGHT_SOURCE_COLOUR,
                         point_one,
                         point_two)


    def __render_light_ray(self, light_ray: Ray):
        # implementation for rendering an invidividual light ray
        # create a pygame line
        LAMBDA_END = 1000 # temporary value for drawing infinite lines without any objects
        pygame.draw.aaline(self.__screen, self.__LIGHT_RAY_COLOUR, light_ray.start_point, light_ray.start_point + LAMBDA_END*light_ray.direction)
        
