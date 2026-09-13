import unittest
import numpy as np
from Optics import snells_law


class TestOptics(unittest.TestCase):
    def test_snells_law(self):
        # Test 1: Normal refraction
        # set up the refractive indices
        n1 = 1.0
        n2 = 1.5
        # set up vectors
        incident_vector = np.array([0.707107, -0.707107])
        normal_vector = np.array([0, 1])
        # find transmitted vector using Snell's law subroutine
        transmitted_vector = snells_law(
            n1, n2, incident_vector, normal_vector
        )

        # use the unittest's library to check if the transmitted vector is as expected
        self.assertAlmostEqual(transmitted_vector[0], 0.471405, places=5)
        self.assertAlmostEqual(transmitted_vector[1], -0.881917, places=5)


        # Test 2: Total internal reflection
        # this test is to make sure that the snell's law function can handle total internal reflection
        n1 = 1.5
        n2 = 1.0
        incident_vector = np.array([0.8, -0.6])
        normal_vector = np.array([0, 1])

        transmitted_vector = snells_law(
            n1, n2, incident_vector, normal_vector
        )

        self.assertAlmostEqual(transmitted_vector[0], 0.8, places=5)
        self.assertAlmostEqual(transmitted_vector[1], 0.6, places=5)


        # Test 3: Boundary / grazing incidence
        # this test cases ensures that the snell's law function can handle boundary data
        n1 = 1.0
        n2 = 1.5
        incident_vector = np.array([1, 0])
        normal_vector = np.array([0, 1])

        transmitted_vector = snells_law(
            n1, n2, incident_vector, normal_vector
        )

        self.assertAlmostEqual(transmitted_vector[0], 1.0, places=5)
        self.assertAlmostEqual(transmitted_vector[1], 0.0, places=5)


        # Test 4: Boundary / approximately critical angle
        n1 = 1.5
        n2 = 1.0
        incident_vector = np.array([0.667, -0.745])
        normal_vector = np.array([0, 1])

        transmitted_vector = snells_law(
            n1, n2, incident_vector, normal_vector
        )

        self.assertAlmostEqual(transmitted_vector[0], 1.0, places=2)
        self.assertAlmostEqual(transmitted_vector[1], 0.0, places=2)


        # Test 5: Erroneous / invalid refractive index
        # This test is to make sure that invalid data raises an error, which can be handled
        # an error is raised so that elsewhere in the program, the error can be handled and the program can continue to run without crashing

        n1 = 0
        n2 = 1.5
        incident_vector = np.array([0, -1])
        normal_vector = np.array([0, 1])

        with self.assertRaises(ValueError):
            snells_law(
                n1, n2, incident_vector, normal_vector
            )


        # Test 6: Erroneous / zero-length normal vector
        # This test is to make sure that invalid data raises an error, which can be handled
        # an error is raised so that elsewhere in the program, the error can be handled and the program can continue to run without crashing
        n1 = 1.0
        n2 = 1.5
        incident_vector = np.array([0, -1])
        normal_vector = np.array([0, 0])

        with self.assertRaises(ValueError):
            snells_law(
                n1, n2, incident_vector, normal_vector
            )

if __name__ == '__main__':
    unittest.main()