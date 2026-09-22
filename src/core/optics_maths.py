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

def fresnel_reflectance(n1, n2, angle):
    # convert the angle to radians
    angle_rad = math.radians(angle)
    # ensure that the refractive indices are positive
    if n1 <= 0 or n2 <= 0 or angle < 0 or angle > 90:
        raise ValueError("Refractive indices must be positive and angle must be between 0 and 90 degrees.")
    # calculate the transmitted angle using Snell's law
    sin_theta_t = (n1/n2) * math.sin(angle_rad)
    
    # check for total internal reflection
    if sin_theta_t > 1:
        return 1.0  # total internal reflection, all light is reflected
    
    # calculate the reflectance intensity using the Fresnel equations
    cos_theta_t = math.sqrt(1 - sin_theta_t**2)
    # calculate the individual reflectance for s and p polarisations as specified in the design section
    R_s = ((n1 * math.cos(angle_rad) - n2 * cos_theta_t) / (n1 * math.cos(angle_rad) + n2 * cos_theta_t))**2
    R_p = ((n1 * cos_theta_t - n2 * math.cos(angle_rad)) / (n1 * cos_theta_t + n2 * math.cos(angle_rad)))**2
    R = (R_s + R_p) / 2  # average reflectance for unpolarized light
    return R

# this must have the wavelength in micrometers and NOT nanometres
def cauchy_equation(A, B, wavelength):
    # validate data
    if A <= 0 or B <= 0 or wavelength <= 0:
        raise ValueError("Values must be positive")

    # calculate value
    value = A + B/(wavelength**2)
    return value
