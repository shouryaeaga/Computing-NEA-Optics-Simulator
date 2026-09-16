import unittest
import numpy as np
from Optics import snells_law, reflection_vector


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

        self.assertAlmostEqual(transmitted_vector[0], 0.666666, places=5)
        self.assertAlmostEqual(transmitted_vector[1], -0.745356, places=5)


        # Test 4: Erroneous / invalid refractive index
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


        # Test 5: Erroneous / zero-length normal vector
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

    def test_reflection_vector(self):
        # Test 1: Normal reflection
        # create input vectors from the test plan
        incident_vector = np.array([0.707107, -0.707107])
        normal_vector = np.array([0, 1])
        # use the subroutine defined the in the Optics.py file to find the reflected vector
        reflected_vector = reflection_vector(
            incident_vector, normal_vector
        )
        # check the output is as expected
        self.assertAlmostEqual(reflected_vector[0], 0.707107, places=5)
        self.assertAlmostEqual(reflected_vector[1], 0.707107, places=5)

        # this is then copied for all the other tests, 
        # with their corresponding inputs and outputs from the test plan

        # Test 2: Angled reflection
        incident_vector = np.array([-0.5, -0.866025])
        normal_vector = np.array([0, 1])

        reflected_vector = reflection_vector(
            incident_vector, normal_vector
        )

        self.assertAlmostEqual(reflected_vector[0], -0.5, places=5)
        self.assertAlmostEqual(reflected_vector[1], 0.866025, places=5)


        # Test 3: Boundary / grazing incidence
        incident_vector = np.array([1, 0])
        normal_vector = np.array([0, 1])

        reflected_vector = reflection_vector(
            incident_vector, normal_vector
        )

        self.assertAlmostEqual(reflected_vector[0], 1.0, places=5)
        self.assertAlmostEqual(reflected_vector[1], 0.0, places=5)


        # Test 4: Erroneous / zero-length normal vector
        incident_vector = np.array([0, -1])
        normal_vector = np.array([0, 0])
        # since this is erroneous data, we expect the subroutine to raise a value error
        # this allows us to then handle the error appropriately in the main program
        # i.e. we can catch the error and display a message to the user
        # this is better than having the program crash

        with self.assertRaises(ValueError):
            reflection_vector(
                incident_vector, normal_vector
            )

if __name__ == '__main__':
    unittest.main()