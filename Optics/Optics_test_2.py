import unittest
import numpy as np
from Optics import reflection_vector
# import required modules

class TestOptics(unittest.TestCase):
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
    # this allows me to run the test from the terminal, running every test in the file
    unittest.main()