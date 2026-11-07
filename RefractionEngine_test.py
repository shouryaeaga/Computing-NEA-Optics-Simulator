import unittest
import sys
from pathlib import Path

import numpy as np

SRC_DIR = Path(__file__).resolve().parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from GUI.refraction_engine import AIR_REFRACTIVE_INDEX, MAX_DEPTH, RefractionEngine
from GUI.scene import Scene
from core.ray import Ray
from objects.glass_shapes.Polygon import Polygon
from objects.light_sources.Base import LightSource


class DummyLightSource(LightSource):
    def __init__(self, rays: list[Ray]):
        super().__init__((0.0, 0.0))
        self.get_emitted_rays().extend(rays)


class TestRefractionEngine(unittest.TestCase):
    def round_values(self, value):
        if isinstance(value, np.ndarray):
            return np.round(value, 5)
        if isinstance(value, tuple):
            return tuple(self.round_values(item) for item in value)
        if isinstance(value, list):
            return [self.round_values(item) for item in value]
        if isinstance(value, float):
            return round(value, 5)
        return value

    def print_input_output(self, subroutine, inputs, output):
        rounded_inputs = self.round_values(inputs)
        rounded_output = self.round_values(output)
        print(
            f"{subroutine} | Input: {rounded_inputs} | Output: {rounded_output}"
        )

    def make_square(self, x1, y1, x2, y2, refractive_index=1.5):
        vertices = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
        return Polygon(vertices, (0, 0), refractive_index)

    def test_calculate_intersection(self):
        scene = Scene()
        engine = RefractionEngine(scene)

        # Test 1: Normal intersection
        ray = Ray((0.0, 0.0), (1.0, 0.0))
        edge = ((5.0, -1.0), (5.0, 1.0))
        point = engine.calculate_intersection(ray, edge)
        self.print_input_output("calculate_intersection", (ray.get_start_point(), ray.get_direction(), edge), point)
        self.assertAlmostEqual(point[0], 5.0, places=5)
        self.assertAlmostEqual(point[1], 0.0, places=5)

        # Test 2: Parallel line (no intersection)
        ray = Ray((0.0, 0.0), (1.0, 0.0))
        edge = ((0.0, 1.0), (5.0, 1.0))
        point = engine.calculate_intersection(ray, edge)
        self.print_input_output("calculate_intersection", (ray.get_start_point(), ray.get_direction(), edge), point)
        self.assertIsNone(point)

        # Test 3: Intersection behind the ray start point
        ray = Ray((0.0, 0.0), (1.0, 0.0))
        edge = ((-1.0, -1.0), (-1.0, 1.0))
        point = engine.calculate_intersection(ray, edge)
        self.print_input_output("calculate_intersection", (ray.get_start_point(), ray.get_direction(), edge), point)
        self.assertIsNone(point)

        # Test 4: Crossing line but edge segment does not contain hit
        ray = Ray((0.0, 0.0), (1.0, 0.0))
        edge = ((5.0, 1.0), (5.0, 2.0))
        point = engine.calculate_intersection(ray, edge)
        self.print_input_output("calculate_intersection", (ray.get_start_point(), ray.get_direction(), edge), point)
        self.assertIsNone(point)

    def test_find_closest_intersection(self):
        # Test 1: choose the closest intersection across multiple polygons
        scene = Scene()
        engine = RefractionEngine(scene)
        near_shape = self.make_square(5, -1, 7, 1)
        far_shape = self.make_square(10, -1, 12, 1)
        scene.add_glass_shape(near_shape)
        scene.add_glass_shape(far_shape)
        ray = Ray((0.0, 0.0), (1.0, 0.0))

        point, shape, edge = engine._RefractionEngine__find_closest_intersection(ray)
        self.print_input_output(
            "__find_closest_intersection",
            (ray.get_start_point(), ray.get_direction(), "two_squares"),
            (point, edge),
        )

        self.assertTrue(np.allclose(point, (5.0, 0.0)))
        self.assertIs(shape, near_shape)
        self.assertAlmostEqual(ray.get_refractive_index(), AIR_REFRACTIVE_INDEX, places=5)

        # Test 2: ray starts inside glass, refractive index should be set to glass
        scene = Scene()
        engine = RefractionEngine(scene)
        glass_shape = self.make_square(-1, -1, 1, 1, refractive_index=1.62)
        scene.add_glass_shape(glass_shape)
        ray = Ray((0.0, 0.0), (1.0, 0.0), refractive_index=AIR_REFRACTIVE_INDEX)

        point, shape, edge = engine._RefractionEngine__find_closest_intersection(ray)
        self.print_input_output(
            "__find_closest_intersection",
            (ray.get_start_point(), ray.get_direction(), "inside_square"),
            (point, edge),
        )

        self.assertTrue(np.allclose(point, (1.0, 0.0)))
        self.assertIs(shape, glass_shape)
        self.assertAlmostEqual(ray.get_refractive_index(), 1.62, places=5)

    def test_get_refracted_ray(self):
        # Test 1: refracted ray is created with updated depth and medium
        scene = Scene()
        engine = RefractionEngine(scene)
        glass_shape = self.make_square(-1, -1, 1, 1, refractive_index=1.5)
        scene.add_glass_shape(glass_shape)
        ray = Ray((0.0, 0.0), (1.0, 0.0), depth=2, refractive_index=1.5)

        refracted_ray, point = engine._RefractionEngine__get_refracted_ray(ray)
        self.print_input_output(
            "__get_refracted_ray",
            (ray.get_start_point(), ray.get_direction(), ray.get_refractive_index()),
            (point, refracted_ray.get_start_point(), refracted_ray.get_direction(), refracted_ray.get_refractive_index()),
        )

        self.assertTrue(np.allclose(point, (1.0, 0.0)))
        self.assertEqual(refracted_ray.get_depth(), 3)
        self.assertAlmostEqual(refracted_ray.get_refractive_index(), AIR_REFRACTIVE_INDEX, places=5)
        self.assertTrue(np.allclose(refracted_ray.get_direction(), (1.0, 0.0)))
        self.assertGreater(refracted_ray.get_start_point()[0], 1.0)

        # Test 2: no geometry hit returns (None, None)
        scene = Scene()
        engine = RefractionEngine(scene)
        ray = Ray((0.0, 0.0), (1.0, 0.0))

        refracted_ray, point = engine._RefractionEngine__get_refracted_ray(ray)
        self.print_input_output(
            "__get_refracted_ray",
            (ray.get_start_point(), ray.get_direction(), "no_glass"),
            (refracted_ray, point),
        )
        self.assertIsNone(refracted_ray)
        self.assertIsNone(point)

    def test_calculate_refractions(self):
        # Test 1: ray escapes the scene and gets default finite draw distance
        scene = Scene()
        engine = RefractionEngine(scene)
        ray = Ray((0.0, 0.0), (1.0, 0.0))
        scene.add_light_source(DummyLightSource([ray]))

        engine.calculate_refractions()
        self.print_input_output(
            "calculate_refractions",
            (ray.get_start_point(), ray.get_direction(), "no_glass"),
            (ray.get_distance(), len(engine.refracted_rays)),
        )

        self.assertEqual(ray.get_distance(), 1000)
        self.assertEqual(len(engine.refracted_rays), 1)

        # Test 2: max depth ray should not spawn new rays
        scene = Scene()
        engine = RefractionEngine(scene)
        ray = Ray((0.0, 0.0), (1.0, 0.0), depth=MAX_DEPTH)
        scene.add_light_source(DummyLightSource([ray]))

        engine.calculate_refractions()
        self.print_input_output(
            "calculate_refractions",
            (ray.get_start_point(), ray.get_direction(), ray.get_depth()),
            (ray.get_distance(), len(engine.refracted_rays)),
        )

        self.assertEqual(ray.get_distance(), 10000)
        self.assertEqual(len(engine.refracted_rays), 1)


if __name__ == "__main__":
    unittest.main()
