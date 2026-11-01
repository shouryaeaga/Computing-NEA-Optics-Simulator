import pygame

from GUI.scene import Scene
from objects.light_sources.Beam import Beam
from objects.light_sources.SingleRay import SingleRay
from objects.glass_shapes.Polygon import Polygon
from objects.glass_shapes.Rectangle import Rectangle

class InputHandler:
    __SELECTION_DISTANCE = 5

    def __init__(self, scene: Scene):
        self.__scene = scene
        self.__dragged_object = None
        self.__dragged_point_index = None

    def handle_event(self, event: pygame.event.Event):
        # handle mouse events for selecting and dragging light sources and glass shapes
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.__start_drag(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.__stop_drag()
        elif event.type == pygame.MOUSEMOTION and self.__dragged_object is None:
            self.__update_hover_state(event.pos)

    def update(self, mouse_position):
        # update and drag the selected object if there is one
        if self.__dragged_object is not None:
            self.__update_dragged_object(mouse_position)

    def __start_drag(self, mouse_position):
        for light_source in self.__scene.get_light_sources():
            for point_index, point in enumerate(
                light_source.get_selectable_points()
            ):
                if self.__is_near_point(mouse_position, point):
                    self.__dragged_object = light_source
                    self.__dragged_point_index = point_index
                    light_source.set_selected(True)
                    return

        for glass_shape in self.__scene.get_glass_shapes():
            for point_index, point in enumerate(
                glass_shape.get_vertices()
            ):
                if self.__is_near_point(mouse_position, point):
                    self.__dragged_object = glass_shape
                    self.__dragged_point_index = point_index
                    glass_shape.set_selected(True)
                    return

    def __stop_drag(self):
        self.__dragged_object = None
        self.__dragged_point_index = None

    def __update_hover_state(self, mouse_position):
        for light_source in self.__scene.get_light_sources():
            # check whether the mouse is near any of the light source's selectable points
            light_source.set_selected(any(
                self.__is_near_point(mouse_position, point)
                for point in light_source.get_selectable_points()
            ))
        for glass_shape in self.__scene.get_glass_shapes():
            # check whether the mouse is near any of the glass shape's vertices
            glass_shape.set_selected(any(
                self.__is_near_point(mouse_position, point)
                for point in glass_shape.get_vertices()
            ))

    # Updates the positions of the dragged object based on the mouse position
    def __update_dragged_object(self, mouse_position):
        dragged_object = self.__dragged_object
        point_index = self.__dragged_point_index
        if issubclass(type(dragged_object), Rectangle):
            dragged_object.update_size(mouse_position, ["tl", "tr", "br", "bl"][point_index])
            return

        if isinstance(dragged_object, Beam):
            endpoints = list(dragged_object.get_endpoints())
            endpoints[point_index] = mouse_position
            dragged_object.update_points(*endpoints)
        elif isinstance(dragged_object, SingleRay) and point_index == 1:
            dragged_object.update_direction(mouse_position)
        elif isinstance(dragged_object, SingleRay):
            dragged_object.update_position(mouse_position)
            dragged_object.update_direction(
                dragged_object.get_selectable_points()[1]
            )
        else:
            dragged_object.update_position(mouse_position)

    def __is_near_point(self, first_point, second_point):
        return (
            abs(first_point[0] - second_point[0]) < self.__SELECTION_DISTANCE
            and abs(first_point[1] - second_point[1]) < self.__SELECTION_DISTANCE
        )
