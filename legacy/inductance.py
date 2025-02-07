import numpy as np


def finite_line(start_x=-3/2, end_x=3/2, current=1.0, point_x=0.0, point_y=0.0):
    """
    Calculate the magnetic field at a point (point_x, point_y) due to a finite line segment
    along the x-axis from start_x to end_x carrying a current I.
    """
    mu_0 = 4 * np.pi * 1e-7  # Permeability of free space
    dl = 1e-3  # Small segment length for numerical integration
    x_values = np.arange(start_x, end_x, dl) # all the x values in steps of dl to integrate over
    Bx, By = 0.0, 0.0 # return values

    for x in x_values:
        # find distance of current point on finite line to the point we calculate the magnetic field at
        # = calculate r
        r_x = point_x - x
        r_y = point_y
        r = np.sqrt(r_x**2 + r_y**2)
        if r == 0:
            continue  # Skip the singularity
        dB = (mu_0 * current * dl) / (2 * np.pi * r**2)
        Bx += -dB * r_y / r
        By += dB * r_x / r

    return Bx, By

# Example usage
start_x = -3 / 2
end_x = 3 / 2
current = 1.0
point_x = 1.0
point_y = 1.0

Bx, By = finite_line(start_x, end_x, current, point_x, point_y)
print(f"Magnetic field at ({point_x}, {point_y}): Bx = {Bx}, By = {By}")
