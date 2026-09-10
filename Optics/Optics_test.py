import unittest
import numpy as np
from Optics import snells_law


class TestOptics(unittest.TestCase):
    def test_snells_law(self):
        n1 = 1.0  # refractive index of medium 1 (air)
        n2 = 1.5  # refractive index of medium 2 (glass)
        incident_vector = np.array([0, -1])  # incident vector pointing downwards
        normal_vector = np.array([0, 1])  # normal vector pointing upwards

        transmitted_vector = snells_law(n1, n2, incident_vector, normal_vector)
        # Check if the transmitted vector is in the expected direction
        self.assertAlmostEqual(transmitted_vector[0], 0.0, places=5)
        self.assertAlmostEqual(transmitted_vector[1], -1.000000, places=5)  # should be pointing upwards      

    def test_snells_laws_2(self):
        n1 = 1.8
        n2 = 2.0
        test_2_incident = np.array([1, -1])  # incident vector at 45 degrees
        normal_vector = np.array([0, 1])  # normal vector pointing upwards
        #normalise the incident vector
        test_2_incident = test_2_incident / np.linalg.norm(test_2_incident)

        transmitted_vector_2 = snells_law(n1, n2, test_2_incident, normal_vector)
        # Check if the transmitted vector is in the expected direction
        self.assertAlmostEqual(transmitted_vector_2[0], 0.636396, places=5)  # should be pointing right
        self.assertAlmostEqual(transmitted_vector_2[1], -0.771362, places=5)  # should be pointing upwards
    def test_snells_laws_3(self):
        n1 = 1.0
        n2 = 1.5
        test_3_incident = np.array([1,0])
        normal_vector = np.array([0,1])
        transmitted_vector_3 = snells_law(n1, n2, test_3_incident, normal_vector)
        self.assertAlmostEqual(transmitted_vector_3[0], 1.0, places=5)
        self.assertAlmostEqual(transmitted_vector_3[1], 0.0, places=5)

if __name__ == '__main__':
    unittest.main()