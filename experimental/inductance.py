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
        B_magnitude (float): Magnitude of the magnetic field.
        B_direction (np.array): Unit vector indicating the direction of the magnetic field.
    """
    B_total = np.array([0.0, 0.0])  # Initialize total magnetic field

    # Sum the contributions of all line segments
    for segment in coil_segments:
        wire_start, wire_end = segment
        B = biot_savart_finite_wire_2d(current, wire_start, wire_end, observation_point, mu0)
        B_total += B

    # Compute magnitude and direction
    B_magnitude = np.linalg.norm(B_total)
    B_direction = B_total / B_magnitude if B_magnitude != 0 else np.array([0.0, 0.0])

    return B_total, B_magnitude, B_direction


def plot_magnetic_field(current, coil_segments, x_range, y_range, resolution=20, plot_type="magnitude"):
    """
    Plot the magnetic field of a coil in the x-y plane.

    Parameters:
        current (float): Current in the coil (in Amperes).
        coil_segments (list): List of line segments, where each segment is a tuple (start, end).
        x_range (tuple): Range of x values (x_min, x_max).
        y_range (tuple): Range of y values (y_min, y_max).
        resolution (int): Number of points along each axis (default is 20).
        plot_type (str): Type of plot ("magnitude" or "direction").
    """
    # Define the grid in the x-y plane
    x = np.linspace(x_range[0], x_range[1], resolution)
    y = np.linspace(y_range[0], y_range[1], resolution)
    X, Y = np.meshgrid(x, y)
    Bx = np.zeros_like(X)
    By = np.zeros_like(Y)
    B_magnitude = np.zeros_like(X)

    # Compute the magnetic field at each point on the grid
    for i in range(len(x)):
        for j in range(len(y)):
            observation_point = np.array([X[i, j], Y[i, j]])  # Observation point in the x-y plane
            B, B_mag, _ = compute_coil_magnetic_field(current, coil_segments, observation_point)
            Bx[i, j] = B[0]  # x-component of the magnetic field
            By[i, j] = B[1]  # y-component of the magnetic field
            B_magnitude[i, j] = B_mag  # Magnitude of the magnetic field

    # Plot the magnetic field
    plt.figure(figsize=(10, 8))

    if plot_type == "magnitude":
        # Contour plot for magnitude
        plt.contourf(X, Y, B_magnitude, levels=50, cmap='viridis')
        plt.colorbar(label='Magnetic Field Magnitude (T)')
        plt.title('Magnetic Field Magnitude of a Coil (x-y plane)')
    elif plot_type == "direction":
        # Quiver plot for direction
        plt.quiver(X, Y, Bx, By, color='b', scale=1e-5, width=0.002)
        plt.streamplot(X, Y, Bx, By, color='r', density=1.5)
        plt.title('Magnetic Field Direction of a Coil (x-y plane)')

    # Plot the coil segments
    for segment in coil_segments:
        start, end = segment
        plt.plot([start[0], end[0]], [start[1], end[1]], 'k-', linewidth=2)

    plt.xlabel('x (m)')
    plt.ylabel('y (m)')
    plt.grid()
    plt.show()


# Example usage
if __name__ == "__main__":
    # Define the coil as a list of line segments
    # coil_segments = [
    # (np.array([0.008, 0.008]), np.array([-0.008, 0.008])),
    # (np.array([-0.008, 0.008]), np.array([-0.008, -0.009])),   # Extended left side
    # (np.array([0.008, -0.008]), np.array([0.008, 0.008])),    # Right side
    # (np.array([-0.008, -0.009]), np.array([0.009, -0.009])),  # Bottom side
    # (np.array([0.009, 0.009]), np.array([-0.009, 0.009])),
    # (np.array([-0.009, 0.009]), np.array([-0.009, -0.01])),   # Extended left side
    # (np.array([0.009, -0.009]), np.array([0.009, 0.009])),    # Right side
    # (np.array([-0.009, -0.01]), np.array([0.01, -0.01])),  # Bottom side
    # (np.array([0.01, -0.01]), np.array([0.01, 0.01])),    # Right side
    # (np.array([0.01, 0.01]), np.array([-0.01, 0.01])),    # Top side
    # (np.array([-0.01, 0.01]), np.array([-0.01, -0.011]))   # Extended left side
    # ]
    # coil_segments = [
    # (np.array([10.34, 10.34]), np.array([9.66, 10.34])),
    # (np.array([9.66, 10.34]), np.array([9.66, 9.66])),
    # (np.array([9.66, 9.66]), np.array([10.60, 9.66])),
    # (np.array([10.60, 9.66]), np.array([10.60, 10.60])),
    # (np.array([10.60, 10.60]), np.array([9.40, 10.60])),
    # (np.array([9.40, 10.60]), np.array([9.40, 9.40])),
    # (np.array([9.40, 9.40]), np.array([10.85, 9.40])),
    # (np.array([10.85, 9.40]), np.array([10.85, 10.85])),
    # (np.array([10.85, 10.85]), np.array([9.15, 10.85])),
    # (np.array([9.15, 10.85]), np.array([9.15, 9.15])),
    # (np.array([9.15, 9.15]), np.array([11.10, 9.15])),
    # (np.array([11.10, 9.15]), np.array([11.10, 11.10])),
    # (np.array([11.10, 11.10]), np.array([8.90, 11.10])),
    # (np.array([8.90, 11.10]), np.array([8.90, 8.90])),
    # (np.array([8.90, 8.90]), np.array([11.36, 8.90])),
    # (np.array([11.36, 8.90]), np.array([11.36, 11.36])),
    # (np.array([11.36, 11.36]), np.array([8.64, 11.36])),
    # (np.array([8.64, 11.36]), np.array([8.64, 8.64])),
    # (np.array([8.64, 8.64]), np.array([11.61, 8.64])),
    # (np.array([11.61, 8.64]), np.array([11.61, 11.61])),
    # (np.array([11.61, 11.61]), np.array([8.39, 11.61])),
    # (np.array([8.39, 11.61]), np.array([8.39, 8.39])),
    # (np.array([8.39, 8.39]), np.array([11.86, 8.39])),
    # (np.array([11.86, 8.39]), np.array([11.87, 11.87])),
    # (np.array([11.87, 11.87]), np.array([8.13, 11.87])),
    # (np.array([8.13, 11.87]), np.array([8.13, 8.13])),
    # (np.array([8.13, 8.13]), np.array([12.12, 8.13])),
    # (np.array([12.12, 8.13]), np.array([12.12, 12.12])),
    # (np.array([12.12, 12.12]), np.array([7.88, 12.12])),
    # (np.array([7.88, 12.12]), np.array([7.88, 7.88])),
    # (np.array([7.88, 7.88]), np.array([12.37, 7.88])),
    # (np.array([12.37, 7.88]), np.array([12.37, 12.37])),
    # (np.array([12.37, 12.37]), np.array([7.63, 12.37])),
    # (np.array([7.63, 12.37]), np.array([7.63, 7.63])),
    # (np.array([7.63, 7.63]), np.array([12.63, 7.63])),
    # (np.array([12.63, 7.63]), np.array([12.63, 12.63]))
    # ]
    coil_segments = [
    (np.array([0.1034, 0.1034]), np.array([0.0966, 0.1034])),
    (np.array([0.0966, 0.1034]), np.array([0.0966, 0.0966])),
    (np.array([0.0966, 0.0966]), np.array([0.1060, 0.0966])),
    (np.array([0.1060, 0.0966]), np.array([0.1060, 0.1060])),
    (np.array([0.1060, 0.1060]), np.array([0.0940, 0.1060])),
    (np.array([0.0940, 0.1060]), np.array([0.0940, 0.0940])),
    (np.array([0.0940, 0.0940]), np.array([0.1085, 0.0940])),
    (np.array([0.1085, 0.0940]), np.array([0.1085, 0.1085])),
    (np.array([0.1085, 0.1085]), np.array([0.0915, 0.1085])),
    (np.array([0.0915, 0.1085]), np.array([0.0915, 0.0915])),
    (np.array([0.0915, 0.0915]), np.array([0.1110, 0.0915])),
    (np.array([0.1110, 0.0915]), np.array([0.1110, 0.1110])),
    (np.array([0.1110, 0.1110]), np.array([0.0890, 0.1110])),
    (np.array([0.0890, 0.1110]), np.array([0.0890, 0.0890])),
    (np.array([0.0890, 0.0890]), np.array([0.1136, 0.0890])),
    (np.array([0.1136, 0.0890]), np.array([0.1136, 0.1136])),
    (np.array([0.1136, 0.1136]), np.array([0.0864, 0.1136])),
    (np.array([0.0864, 0.1136]), np.array([0.0864, 0.0864])),
    (np.array([0.0864, 0.0864]), np.array([0.1161, 0.0864])),
    (np.array([0.1161, 0.0864]), np.array([0.1161, 0.1161])),
    (np.array([0.1161, 0.1161]), np.array([0.0839, 0.1161])),
    (np.array([0.0839, 0.1161]), np.array([0.0839, 0.0839])),
    (np.array([0.0839, 0.0839]), np.array([0.1186, 0.0839])),
    (np.array([0.1186, 0.0839]), np.array([0.1187, 0.1187])),
    (np.array([0.1187, 0.1187]), np.array([0.0813, 0.1187])),
    (np.array([0.0813, 0.1187]), np.array([0.0813, 0.0813])),
    (np.array([0.0813, 0.0813]), np.array([0.1212, 0.0813])),
    (np.array([0.1212, 0.0813]), np.array([0.1212, 0.1212])),
    (np.array([0.1212, 0.1212]), np.array([0.0788, 0.1212])),
    (np.array([0.0788, 0.1212]), np.array([0.0788, 0.0788])),
    (np.array([0.0788, 0.0788]), np.array([0.1237, 0.0788])),
    (np.array([0.1237, 0.0788]), np.array([0.1237, 0.1237])),
    (np.array([0.1237, 0.1237]), np.array([0.0763, 0.1237])),
    (np.array([0.0763, 0.1237]), np.array([0.0763, 0.0763])),
    (np.array([0.0763, 0.0763]), np.array([0.1263, 0.0763])),
    (np.array([0.1263, 0.0763]), np.array([0.1263, 0.1263]))
    ]


    # Parameters
    current = 1.0  # Current in the coil (Amperes)
    # x_range = (-0.025, 0.025)  # x from -2.5 cm to +2.5 cm
    # y_range = (-0.025, 0.025)  # y from -2.5 cm to +2.5 cm
    x_range = (0.06, 0.15)
    y_range = (0.06, 0.15)

    # Plot the magnetic field magnitude
    plot_magnetic_field(current, coil_segments, x_range, y_range, plot_type="magnitude")

    # Plot the magnetic field direction
    plot_magnetic_field(current, coil_segments, x_range, y_range, plot_type="direction")