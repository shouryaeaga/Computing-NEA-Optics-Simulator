import numpy as np
import math

# Snell's law in vector form
def snells_law(n1, n2, incident_vector, normal_vector):
    # find the ratio between the refractive indices
    mu = n1/n2
    # find angle between the incident vector and the normal vector
    cos_theta_i = -np.dot(normal_vector, incident_vector)

    # find transmitted vector using Snell's law in vector form
    transmitted_vector = math.sqrt(1-mu**2 * (1 - cos_theta_i**2)) * normal_vector + mu * incident_vector
    # return the vector result
    return transmitted_vector


