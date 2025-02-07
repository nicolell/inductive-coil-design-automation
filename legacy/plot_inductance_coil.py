import numpy as np
import matplotlib.pyplot as plt

def biot_savart_finite_wire_2d(current, wire_start, wire_end, observation_point, mu0=4 * np.pi * 1e-7):
    """
    Compute the magnetic field at a point in the x-y plane due to a finite straight wire using the Biot-Savart Law.

    Parameters:
        current (float): Current in the wire (in Amperes).
        wire_start (np.array): Start point of the wire as a 2D vector [x1, y1].
        wire_end (np.array): End point of the wire as a 2D vector [x2, y2].
        observation_point (np.array): Point where the magnetic field is calculated [x, y].
        mu0 (float): Permeability of free space (default is 4π × 10^-7 Tm/A).

    Returns:
        B (np.array): Magnetic field vector at the observation point [Bx, By].
    """
    # Convert inputs to numpy arrays
    wire_start = np.array(wire_start)
    wire_end = np.array(wire_end)
    observation_point = np.array(observation_point)

    # Vector along the wire
    dl = wire_end - wire_start
    length_wire = np.linalg.norm(dl)
    dl_unit = dl / length_wire  # Unit vector along the wire

    # Vector from the wire start to the observation point
    r_start = observation_point - wire_start
    # Vector from the wire end to the observation point
    r_end = observation_point - wire_end

    # Distance from the observation point to the wire start and end
    r_start_mag = np.linalg.norm(r_start)
    r_end_mag = np.linalg.norm(r_end)

    # Cross product of dl_unit and r_start / r_end (in 2D, cross product is a scalar)
    cross_start = dl_unit[0] * r_start[1] - dl_unit[1] * r_start[0]
    cross_end = dl_unit[0] * r_end[1] - dl_unit[1] * r_end[0]

    # Biot-Savart Law for a finite wire in 2D
    B_magnitude = (mu0 * current) / (4 * np.pi) * (
        cross_start / (r_start_mag * (r_start_mag - np.dot(dl_unit, r_start))) -
        cross_end / (r_end_mag * (r_end_mag - np.dot(dl_unit, r_end)))
    )

    # Direction of the magnetic field (perpendicular to the wire and observation point)
    B_direction = np.array([-r_start[1], r_start[0]])  # Rotate r_start by 90 degrees
    B_direction /= np.linalg.norm(B_direction)  # Normalize

    # Magnetic field vector
    B = B_magnitude * B_direction

    return B


def compute_coil_magnetic_field(current, coil_segments, observation_point, mu0=4 * np.pi * 1e-7):
    """
    Compute the magnetic field at a point due to a coil made up of multiple finite line segments.

    Parameters:
        current (float): Current in the coil (in Amperes).
        coil_segments (list): List of line segments, where each segment is a tuple (start, end).
        observation_point (np.array): Point where the magnetic field is calculated [x, y].
        mu0 (float): Permeability of free space (default is 4π × 10^-7 Tm/A).

    Returns:
        B_total (np.array): Total magnetic field vector at the observation point [Bx, By].
    """
    B_total = np.array([0.0, 0.0])  # Initialize total magnetic field

    # Sum the contributions of all line segments
    for segment in coil_segments:
        wire_start, wire_end = segment
        B = biot_savart_finite_wire_2d(current, wire_start, wire_end, observation_point, mu0)
        B_total += B

    return B_total


# Define the coil as a list of line segments
coil_segments = [
    (np.array([0.008, 0.008]), np.array([-0.008, 0.008])),
    (np.array([-0.008, 0.008]), np.array([-0.008, -0.009])),   # Extended left side
    (np.array([0.008, -0.008]), np.array([0.008, 0.008])),    # Right side
    (np.array([-0.008, -0.009]), np.array([0.009, -0.009])),  # Bottom side
    (np.array([0.009, 0.009]), np.array([-0.009, 0.009])),
    (np.array([-0.009, 0.009]), np.array([-0.009, -0.01])),   # Extended left side
    (np.array([0.009, -0.009]), np.array([0.009, 0.009])),    # Right side
    (np.array([-0.009, -0.01]), np.array([0.01, -0.01])),  # Bottom side
    (np.array([0.01, -0.01]), np.array([0.01, 0.01])),    # Right side
    (np.array([0.01, 0.01]), np.array([-0.01, 0.01])),    # Top side
    (np.array([-0.01, 0.01]), np.array([-0.01, -0.011]))   # Extended left side
]

# Parameters
current = 1.0  # Current in the coil (Amperes)

# Define the grid in the x-y plane
x = np.linspace(-0.025, 0.025, 20)  # x from -2.5 cm to +2.5 cm
y = np.linspace(-0.025, 0.025, 20)  # y from -2.5 cm to +2.5 cm
X, Y = np.meshgrid(x, y)
Bx = np.zeros_like(X)
By = np.zeros_like(Y)

# Compute the magnetic field at each point on the grid
for i in range(len(x)):
    for j in range(len(y)):
        observation_point = np.array([X[i, j], Y[i, j]])  # Observation point in the x-y plane
        B = compute_coil_magnetic_field(current, coil_segments, observation_point)
        Bx[i, j] = B[0]  # x-component of the magnetic field
        By[i, j] = B[1]  # y-component of the magnetic field

# Plot the magnetic field
plt.figure(figsize=(10, 8))
plt.quiver(X, Y, Bx, By, color='b', scale=1e-5, width=0.002)  # Quiver plot for direction
plt.streamplot(X, Y, Bx, By, color='r', density=1.5)  # Streamlines for visualization

# Plot the coil segments
for segment in coil_segments:
    start, end = segment
    plt.plot([start[0], end[0]], [start[1], end[1]], 'k-', linewidth=2)

plt.xlabel('x (m)')
plt.ylabel('y (m)')
plt.title('Magnetic Field of a Coil (x-y plane)')
plt.grid()
plt.show()