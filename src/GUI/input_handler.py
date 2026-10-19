import pygame

from GUI.scene import Scene
from objects.light_sources.Beam import Beam
from objects.light_sources.SingleRay import SingleRay
from objects.glass_shapes.Polygon import Polygon
from objects.glass_shapes.Rectangle import Rectangle

class InputHandler:
    SELECTION_DISTANCE = 5

    def __init__(self, scene: Scene):
        self.scene = scene
        self.dragged_object = None
        self.dragged_point_index = None

    def handle_event(self, event: pygame.event.Event):
        # handle mouse events for selecting and dragging light sources and glass shapes
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.start_drag(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.stop_drag()
        elif event.type == pygame.MOUSEMOTION and self.dragged_object is None:
            self.update_hover_state(event.pos)

    def update(self, mouse_position):
        # update and drag the selected object if there is one
        if self.dragged_object is not None:
            self.update_dragged_object(mouse_position)

    def start_drag(self, mouse_position):
        for light_source in self.scene.get_light_sources():
            for point_index, point in enumerate(
                light_source.get_selectable_points()
            ):
                if self.is_near_point(mouse_position, point):
                    self.dragged_object = light_source
                    self.dragged_point_index = point_index
                    light_source.being_selected = True
                    return

        for glass_shape in self.scene.get_glass_shapes():
            for point_index, point in enumerate(
                glass_shape.get_vertices()
            ):
                if self.is_near_point(mouse_position, point):
                    self.dragged_object = glass_shape
                    self.dragged_point_index = point_index
                    glass_shape.being_selected = True
                    return

    def stop_drag(self):
        self.dragged_object = None
        self.dragged_point_index = None

    def update_hover_state(self, mouse_position):
        for light_source in self.scene.get_light_sources():
            # check whether the mouse is near any of the light source's selectable points
            light_source.being_selected = any(
                self.is_near_point(mouse_position, point)
                for point in light_source.get_selectable_points()
            )
        for glass_shape in self.scene.get_glass_shapes():
            # check whether the mouse is near any of the glass shape's vertices
            glass_shape.being_selected = any(
                self.is_near_point(mouse_position, point)
                for point in glass_shape.get_vertices()
            )

    def update_dragged_object(self, mouse_position):
        object = self.dragged_object
        point_index = self.dragged_point_index
        if issubclass(type(object), Rectangle):
            print("Updating rectangle size")
            object.update_size(mouse_position, ["tl", "tr", "br", "bl"][point_index])
            print(object.width, object.height, object.position)
            return

        if isinstance(object, Beam):
            endpoints = list(object.get_endpoints())
            endpoints[point_index] = mouse_position
            object.update_points(*endpoints)
        elif isinstance(object, SingleRay) and point_index == 1:
            object.update_direction(mouse_position)
        elif isinstance(object, SingleRay):
            object.update_position(mouse_position)
            object.update_direction(
                object.get_selectable_points()[1]
            )
        else:
            object.update_position(mouse_position)

    def is_near_point(self, first_point, second_point):
        return (
            abs(first_point[0] - second_point[0]) < self.SELECTION_DISTANCE
            and abs(first_point[1] - second_point[1]) < self.SELECTION_DISTANCE
        )
