import numpy as np

from core.ray import Ray
from GUI.scene import Scene
from objects.glass_shapes.Polygon import Polygon
from core.optics_maths import snells_law
from collections import deque

MAX_DEPTH = 25
AIR_REFRACTIVE_INDEX = 1.0

class RefractionEngine:
    def __init__(self, scene: Scene):
        self.__scene = scene
        self.refracted_rays: list[Ray] = []  # Store the refracted rays in the scene

    def calculate_refractions(self):
        queue = deque()
        for light_source in self.__scene.get_light_sources():
            queue.extend(light_source.get_emitted_rays())

        while queue:
            ray = queue.popleft()
            self.refracted_rays.append(ray)  # every ray is stored exactly once

            # we only want to refract rays that have not reached the maximum depth
            if ray.get_depth() >= MAX_DEPTH:
                continue

            refracted_ray, point = self.__get_refracted_ray(ray)
            if refracted_ray is None:  # ray escaped the scene, leave it at its default length
                ray.set_distance(1000)
                continue

            # make this ray end at the intersection point, so it does not continue.
            start = np.array(ray.get_start_point(), dtype=float)
            ray.set_distance(np.linalg.norm(np.array(point) - start))
            queue.append(refracted_ray)

                
    def __get_refracted_ray(self, ray: Ray):
        # we need to find the closest intersection point
        point, glass_shape, edge = self.__find_closest_intersection(ray)
        if point is not None and glass_shape is not None:
            # refracted ray must now be calculated based on the intersection point and the normal of the glass shape's edge at that point
            edge_start, edge_end = edge
            edge_vector = np.array(edge_end) - np.array(edge_start)
            # normal vector must be perpendicular to the edge vector
            # it must also be point towards where the ray came from, as that is how the utility libraries work.
            normal_vector = np.array([-edge_vector[1], edge_vector[0]], dtype=float)
            normal_vector /= np.linalg.norm(normal_vector)
            # check if the normal vector is pointing towards the ray's start point, if not,
            # then we need to flip the normal vector
            # Flip it when it points in the same direction as the ray.
            if np.dot(normal_vector, np.array(ray.get_direction())) > 0:
                normal_vector = -normal_vector
            # Use the current medium to determine whether this is an entry or exit.
            n1 = ray.get_refractive_index()
            glass_index = glass_shape.get_refractive_index()
            if np.isclose(n1, glass_index):
                n2 = AIR_REFRACTIVE_INDEX
            else:
                n2 = glass_index
            new_direction = snells_law(
                n1, n2, np.array(ray.get_direction(), dtype=float), normal_vector
            )
            # Total internal reflection does not change the ray's medium.
            cos_theta_i = -np.dot(normal_vector, ray.get_direction())
            square_root_term = 1 - (n1 / n2) ** 2 * (1 - cos_theta_i**2)
            next_refractive_index = n1 if square_root_term < 0 else n2
            # the new ray must start at intersection point but a little further, so it does not bug out
            # as refraction point will be on the edge and so it will intersect and think it is still in the glass shape

            next_start = np.array(point) + new_direction * 1e-6
            refracted_ray = Ray(
                next_start,
                new_direction,
                ray.get_wavelength(),
                ray.get_intensity(),
                ray.get_depth() + 1,
                next_refractive_index,
            )
            return refracted_ray, point
        return None, None  # no intersection point found, so the ray escapes the scene

    def __find_closest_intersection(self, ray: Ray):
        # loop through all glass shapes
        closest_intersection_point = None
        closest_glass_shape = None
        closest_distance = None
        closest_edge = None
        inside_glass_shape = False
        for glass_shape in self.__scene.get_glass_shapes():
            # check if the glass shape is a polygon
            intersection_points = []
            if isinstance(glass_shape, Polygon):
                # these are shortest distance and closest intersection point for this glass shape
                shortest_distance_glass = None
                closest_intersection_point_glass = None
                edges = glass_shape.get_edges()
                closest_edge_glass = None
                # loop through edges to see which is the closest intersection point
                for edge in edges:
                    intersection_point = self.calculate_intersection(ray, edge)
                    # if there is an intersection point, get get the closest one
                    if intersection_point is None:
                        continue
                    if not any(
                        np.allclose(intersection_point, known_point, atol=1e-9)
                        for known_point in intersection_points
                    ):
                        intersection_points.append(intersection_point)
                    compared_distance = np.linalg.norm(np.array(intersection_point) - np.array(ray.get_start_point()))
                    if shortest_distance_glass is None or compared_distance < shortest_distance_glass:
                        shortest_distance_glass = compared_distance
                        closest_intersection_point_glass = intersection_point
                        closest_edge_glass = edge
                # if the closest intersection point for this glass shape is closer
                # than the other glass shapes, then update the closest intersection point and glass shape
                if shortest_distance_glass is not None and (closest_distance is None or shortest_distance_glass < closest_distance):
                    closest_distance = shortest_distance_glass
                    closest_intersection_point = closest_intersection_point_glass
                    closest_glass_shape = glass_shape
                    closest_edge = closest_edge_glass
            # if the ray is inside the polygon, then the number of intersections should be odd
            # so we can set the ray's refractive index to the glass shape's refractive index
            # this is known as the Ray Casting algorithm
            number_of_intersections = len(intersection_points)
            if number_of_intersections % 2 == 1:
                ray.set_refractive_index(glass_shape.get_refractive_index())
                inside_glass_shape = True

        # Emitted rays are reused when their light source moves. Reset the
        # medium when the start point is no longer inside a glass shape.
        if not inside_glass_shape:
            ray.set_refractive_index(AIR_REFRACTIVE_INDEX)
        return closest_intersection_point, closest_glass_shape, closest_edge


    def calculate_intersection(self, ray: Ray, edge: tuple[tuple[int, int], tuple[int, int]]) -> tuple[float, float] | None:
        # this sets up a system of equations that can be solved by linear algebra
        r = np.array(ray.get_start_point(), dtype=float) # ray start point
        d = np.array(ray.get_direction(), dtype=float) # ray direction vector
        a, b = (np.array(p, dtype=float) for p in edge) # edge endpoints
        e = b - a # edge direction vector

        try:
            # this solves the equation r + t*d = a + u*e for t and u, where t is distance along the ray and u is is the distance along the edge
            t, u = np.linalg.solve(np.column_stack((d, -e)), a - r)
        except np.linalg.LinAlgError:  # singular matrix, so parallel
            return None

        # ensure the solutions are valid, as the value of u can only be between 0 and 1
        # and t must be positive, as the ray is a half line
        if t < 0 or not 0 <= u <= 1:
            return None
        return tuple(r + t * d) # return the intersection point as a tuple of floats
