import numpy as np
import math

# requires an incident vector and a normal vector (normalised) to find the reflected vector
# this was defined in design
def reflection_vector(incident_vector, normal_vector):
    # use the formula for reflection r = d - 2(d . n)n
    reflected_vector = incident_vector - 2 * np.dot(incident_vector, normal_vector) * normal_vector
    if np.linalg.norm(normal_vector) == 0:
        raise ValueError("Normal vector cannot be zero-length.")
    return reflected_vector

# Snell's law in vector form
def snells_law(n1, n2, incident_vector, normal_vector):
    # check for invalid refractive indices
    if n1 <= 0 or n2 <= 0:
        raise ValueError("Refractive indices must be positive.")
    # check for zero-length vectors
    if np.linalg.norm(normal_vector) == 0 or np.linalg.norm(incident_vector) == 0:
        raise ValueError("Normal vector cannot be zero-length.")

    # find the ratio between the refractive indices
    mu = n1/n2
    # find angle between the incident vector and the normal vector
    cos_theta_i = -np.dot(normal_vector, incident_vector)

    # calcualate the square root term to check for total internal reflection
    square_root_term = 1 - mu**2 * (1 - cos_theta_i**2)
    if square_root_term < 0: # indicates total internal reflection
        # calculate the reflection vector and return it.
        return reflection_vector(incident_vector, normal_vector)
        
    # find transmitted vector using Snell's law in vector form
    transmitted_vector = mu*incident_vector + (mu * cos_theta_i - math.sqrt(square_root_term)) * normal_vector

    # return the vector result
    return transmitted_vector


