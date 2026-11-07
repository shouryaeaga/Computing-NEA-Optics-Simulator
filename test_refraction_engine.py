import sys
import unittest
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
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


def make_square(x1, y1, x2, y2, refractive_index=1.5):
    vertices = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
    return Polygon(vertices, (0, 0), refractive_index)


class TestRefractionEngine(unittest.TestCase):
    def setUp(self):
        self.scene = Scene()
        self.engine = RefractionEngine(self.scene)

    def test_calculate_intersection_returns_hit_point(self):
        ray = Ray((0.0, 0.0), (1.0, 0.0))
        edge = ((5.0, -1.0), (5.0, 1.0))
        point = self.engine.calculate_intersection(ray, edge)
        self.assertEqual(point, (5.0, 0.0))

    def test_calculate_intersection_returns_none_for_parallel_line(self):
        ray = Ray((0.0, 0.0), (1.0, 0.0))
        edge = ((0.0, 1.0), (5.0, 1.0))
        point = self.engine.calculate_intersection(ray, edge)
        self.assertIsNone(point)

    def test_calculate_intersection_returns_none_when_behind_ray(self):
        ray = Ray((0.0, 0.0), (1.0, 0.0))
        edge = ((-1.0, -1.0), (-1.0, 1.0))
        point = self.engine.calculate_intersection(ray, edge)
        self.assertIsNone(point)

    def test_find_closest_intersection_prefers_nearest_shape(self):
        near_shape = make_square(5, -1, 7, 1)
        far_shape = make_square(10, -1, 12, 1)
        self.scene.add_glass_shape(near_shape)
        self.scene.add_glass_shape(far_shape)
        ray = Ray((0.0, 0.0), (1.0, 0.0))

        point, shape, _ = self.engine._RefractionEngine__find_closest_intersection(ray)

        self.assertTrue(np.allclose(point, (5.0, 0.0)))
        self.assertIs(shape, near_shape)
        self.assertEqual(ray.get_refractive_index(), AIR_REFRACTIVE_INDEX)

    def test_find_closest_intersection_sets_glass_medium_when_inside(self):
        glass_shape = make_square(-1, -1, 1, 1, refractive_index=1.62)
        self.scene.add_glass_shape(glass_shape)
        ray = Ray((0.0, 0.0), (1.0, 0.0), refractive_index=AIR_REFRACTIVE_INDEX)

        point, _, _ = self.engine._RefractionEngine__find_closest_intersection(ray)

        self.assertTrue(np.allclose(point, (1.0, 0.0)))
        self.assertAlmostEqual(ray.get_refractive_index(), 1.62)

    def test_get_refracted_ray_returns_next_ray_and_point(self):
        glass_shape = make_square(-1, -1, 1, 1, refractive_index=1.5)
        self.scene.add_glass_shape(glass_shape)
        ray = Ray((0.0, 0.0), (1.0, 0.0), depth=2, refractive_index=1.5)

        refracted_ray, point = self.engine._RefractionEngine__get_refracted_ray(ray)

        self.assertTrue(np.allclose(point, (1.0, 0.0)))
        self.assertIsNotNone(refracted_ray)
        self.assertEqual(refracted_ray.get_depth(), 3)
        self.assertAlmostEqual(refracted_ray.get_refractive_index(), AIR_REFRACTIVE_INDEX)
        self.assertTrue(np.allclose(refracted_ray.get_direction(), (1.0, 0.0)))
        self.assertGreater(refracted_ray.get_start_point()[0], 1.0)

    def test_calculate_refractions_sets_escape_distance_without_glass(self):
        ray = Ray((0.0, 0.0), (1.0, 0.0))
        self.scene.add_light_source(DummyLightSource([ray]))

        self.engine.calculate_refractions()

        self.assertEqual(ray.get_distance(), 1000)
        self.assertEqual(len(self.engine.refracted_rays), 1)

    def test_calculate_refractions_skips_recursion_at_max_depth(self):
        ray = Ray((0.0, 0.0), (1.0, 0.0), depth=MAX_DEPTH)
        self.scene.add_light_source(DummyLightSource([ray]))

        self.engine.calculate_refractions()

        self.assertEqual(len(self.engine.refracted_rays), 1)
        self.assertEqual(ray.get_distance(), 10000)


if __name__ == "__main__":
    unittest.main()
