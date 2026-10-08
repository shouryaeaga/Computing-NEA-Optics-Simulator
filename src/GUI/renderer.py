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
        # constants to define certain colours
        self.__LIGHT_SOURCE_COLOUR = (255, 245, 182)
        self.__LIGHT_SOURCE_RADIUS = 5
        self.__LIGHT_RAY_COLOUR = (255, 245, 182)
        self.__SQUARE_POINT_SIZE = 5
        self.__UNSELECTED_SQUARE_COLOUR = (255, 0, 0)
        self.__SELECTED_SQUARE_COLOUR = (0, 255, 0)

        # single ray
        test_light_source = SingleRay((50, 50), (100, 100), point_source_radius=self.__LIGHT_SOURCE_RADIUS)

        # point source
        #test_light_source = PointSource((400, 300), point_source_radius=self.__LIGHT_SOURCE_RADIUS)

        #beam
        #test_light_source = Beam((300, 350), (350, 400), 5)

        self.__scene.add_light_source(test_light_source)

        while True:
            self.__render_scene()  # Continuously render the scene in a loop

    def __render_scene(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            # get mouse input to update the location of light sources points
            if event.type == pygame.MOUSEMOTION:
                self.__handle_mouse_hovers(event)

        # Read the current button state each frame. A local variable set by
        # button events would be reset on every call to this method.
        mouse_down = pygame.mouse.get_pressed()[0]
        mouse_position = pygame.mouse.get_pos()

        if mouse_down:
            print("Hi 1")
            for light_source in self.__scene.get_light_sources():
                if light_source.being_selected:
                    if isinstance(light_source, SingleRay):
                        # determine which point is being selected and update it
                        point_position, direction_point = light_source.get_selectable_points()
                        if (
                            abs(mouse_position[0] - direction_point[0]) < self.__SQUARE_POINT_SIZE
                            and abs(mouse_position[1] - direction_point[1]) < self.__SQUARE_POINT_SIZE
                        ):
                            # Update the direction point of the light source to the mouse position
                            light_source.update_direction(mouse_position)
                        elif (
                            abs(mouse_position[0] - point_position[0]) < self.__SQUARE_POINT_SIZE
                            and abs(mouse_position[1] - point_position[1]) < self.__SQUARE_POINT_SIZE
                        ):
                            # Update the position of the light source to the mouse position
                            light_source.update_position(mouse_position)
                            # Recalculate the direction vector based on the new position
                            light_source.update_direction(light_source.get_selectable_points()[1])
                    
        else:
            print("Stopped holding down")
        # Iterate through all light sources in the scene and emit rays
        self.__screen.fill(self.__background_color)  # Clear the screen with the background color

        # call subroutine to handle light sources
        self.__render_light_sources()
        
        pygame.display.flip()
        self.__clock.tick(60)

    def __handle_mouse_hovers(self, event):
        # check whether it is hovering over a light source point
        for light_source in self.__scene.get_light_sources():
            if isinstance(light_source, SingleRay):
                selectable_points = light_source.get_selectable_points()
                for point in selectable_points:
                    if (
                        abs(event.pos[0] - point[0]) < self.__SQUARE_POINT_SIZE
                        and abs(event.pos[1] - point[1]) < self.__SQUARE_POINT_SIZE
                    ):
                        # update the direction point of the light source to the mouse position
                        light_source.being_selected = True
                        break  # Exit the loop after finding the first point that is being hovered over
                    else:
                        light_source.being_selected = False
            elif isinstance(light_source, Beam):
                selectable_points = light_source.get_selectable_points()
                for point in selectable_points:
                    if (
                        abs(event.pos[0] - point[0]) < self.__SQUARE_POINT_SIZE
                        and abs(event.pos[1] - point[1]) < self.__SQUARE_POINT_SIZE
                    ):
                        # update the direction point of the light source to the mouse position
                        light_source.being_selected = True
                        break # break after finding the first point being hovered over
                    else:
                        light_source.being_selected = False
            elif isinstance(light_source, PointSource):
                selectable_points = light_source.get_selectable_points()
                for point in selectable_points:
                    if (
                        abs(event.pos[0] - point[0]) < self.__SQUARE_POINT_SIZE
                        and abs(event.pos[1] - point[1]) < self.__SQUARE_POINT_SIZE
                    ):
                        # update the direction point of the light source to the mouse position
                        light_source.being_selected = True
                    else:
                        light_source.being_selected = False
        
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
        pygame.draw.line(self.__screen,
                         self.__LIGHT_SOURCE_COLOUR,
                         point_one,
                         point_two, width=3)


    def __render_light_ray(self, light_ray: Ray):
        # implementation for rendering an invidividual light ray
        # create a pygame line
        LAMBDA_END = 1000 # temporary value for drawing infinite lines without any objects
        pygame.draw.line(self.__screen, self.__LIGHT_RAY_COLOUR, light_ray.start_point, light_ray.start_point + LAMBDA_END*light_ray.direction,
                         width=3)
        
