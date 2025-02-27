'''
more magnetic field plotting using the data gathered with the tool in biot_savart_v4_3.py
https://github.com/vuthalab/biot-savart
'''
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy.interpolate import griddata
import biot_savart_v4_3 as bs


def plot_3d_fields(Bfields, box_size, start_point, vol_resolution, stride=2):
    '''
    Plots the magnetic field vectors in 3D space.

    Bfields: A 4D array of the Bfield.
    box_size: (x, y, z) dimensions of the box in cm
    start_point: (x, y, z) = (0, 0, 0) = bottom left corner position of the box AKA the offset
    vol_resolution: Division of volumetric meshgrid (generate a point every volume_resolution cm)
    stride: Step size for sampling the field vectors to avoid clutter in the plot.
    '''
    # Generate the grid points
    x = np.linspace(start_point[0], box_size[0] + start_point[0], int(box_size[0]/vol_resolution)+1)
    y = np.linspace(start_point[1], box_size[1] + start_point[1], int(box_size[1]/vol_resolution)+1)
    z = np.linspace(start_point[2], box_size[2] + start_point[2], int(box_size[2]/vol_resolution)+1)
    
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
    
    # Sample the field vectors
    X_sample = X[::stride, ::stride, ::stride]
    Y_sample = Y[::stride, ::stride, ::stride]
    Z_sample = Z[::stride, ::stride, ::stride]
    Bx_sample = Bfields[::stride, ::stride, ::stride, 0]
    By_sample = Bfields[::stride, ::stride, ::stride, 1]
    Bz_sample = Bfields[::stride, ::stride, ::stride, 2]

    # Create the 3D plot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot the field vectors
    # Color by azimuthal angle
    c = np.arctan2(By_sample, Bx_sample)
    # Flatten and normalize
    c = (c.ravel() - c.min()) / c.ptp()
    # Repeat for each body line and two head lines
    c = np.concatenate((c, np.repeat(c, 2)))
    # Colormap
    c = plt.cm.seismic(c)
    ax.quiver(X_sample, Y_sample, Z_sample, Bx_sample, By_sample, Bz_sample, length=0.5, normalize=True ,color=c)
    
    # Set labels
    ax.set_xlabel('X (cm)')
    ax.set_ylabel('Y (cm)')
    ax.set_zlabel('Z (cm)')
    ax.set_title('3D Magnetic Field Vectors')
    
    plt.show()    


def plot_3d_fields3(Bfields, box_size, start_point, vol_resolution, stride=1, level=0):
    # Generate the grid
    X = np.linspace(start_point[0], box_size[0] + start_point[0], int(box_size[0]/vol_resolution)+1)
    Y = np.linspace(start_point[1], box_size[1] + start_point[1], int(box_size[1]/vol_resolution)+1)
    Z = np.linspace(start_point[2], box_size[2] + start_point[2], int(box_size[2]/vol_resolution)+1)

    # Create a meshgrid for 3D plotting
    X, Y, Z = np.meshgrid(X, Y, Z, indexing='ij')

    # Extract the Bz component for plotting
    Bz = Bfields[:, :, :, 2]
    #print(Bz)

    # Flatten the grid and Bz data for 3D plotting
    X_flat = X.flatten()
    Y_flat = Y.flatten()
    Z_flat = Z.flatten()
    Bz_flat = Bz.flatten()

    # Filter points based on the specified level (default: z = 0)
    mask_level = np.isclose(Z_flat, level, atol=vol_resolution/2)  # Allow for small floating-point tolerance
    X_flat = X_flat[mask_level]
    Y_flat = Y_flat[mask_level]
    Bz_flat = Bz_flat[mask_level]

    # Normalize Bz intensity so that the maximum value is 1
    Bz_flat_normalized = Bz_flat / np.max(np.abs(Bz_flat))

    # Create a finer regular grid for interpolation
    grid_resolution = vol_resolution / 6  # Increase resolution
    grid_x, grid_y = np.meshgrid(
        np.linspace(start_point[0], box_size[0] + start_point[0], int(box_size[0]/grid_resolution)+1),
        np.linspace(start_point[1], box_size[1] + start_point[1], int(box_size[1]/grid_resolution)+1),
        indexing='ij'
    )

    # Interpolate Bz intensity onto the finer regular grid
    grid_Bz_normalized = griddata((X_flat, Y_flat), Bz_flat_normalized, (grid_x, grid_y), method='cubic')
    # print(grid_Bz_normalized)
    # coords = zip(grid_x, grid_y, grid_Bz_normalized)
    # for tup in coords:
    #     print(tup)
    # Create a 3D plot
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Create a surface plot with Bz as the third axis
    surf = ax.plot_surface(grid_x, grid_y, grid_Bz_normalized, 
                           facecolors=cm.plasma(grid_Bz_normalized),  # Color based on normalized Bz
                           rstride=1, cstride=1,  # High resolution
                           linewidth=0, 
                           antialiased=True, 
                           shade=True)

    # Add color bar
    sm = plt.cm.ScalarMappable(cmap=plt.cm.plasma)
    sm.set_array(grid_Bz_normalized)
    cbar = fig.colorbar(sm, ax=ax, shrink=0.5, aspect=5)
    cbar.set_label('Normalized Bz Intensity (Max = 1)')

    # Labels and title
    ax.set_xlabel('X (cm)')
    ax.set_ylabel('Y (cm)')
    ax.set_zlabel('Bz')
    ax.set_title(f'3D Magnetic Field Bz at Z = {level} (Bz as Third Axis)')

    plt.show()


def magnetic_field(module_name, left_upper_corner, diameter, plane, level):
	x,y = left_upper_corner
	box = diameter
	bs.write_target_volume(f"{module_name}.txt", f"{module_name}_targetvol", (box, box, 5), (x, y, -2.5), 1, 1)
	# generates a target volume from the coil stored at coil.txt
	# uses 1 cm resolution

	bs.plot_coil(f"{module_name}.txt")
	# plots the coil stored at coil.txt

	volume = bs.read_target_volume(f"{module_name}_targetvol")
	# reads the volume we created
    
	bs.plot_fields(volume, (box, box, 5), (x, y, -2.5), 1, which_plane=plane, level=level, num_contours=50)
	plot_3d_fields(volume, (box, box, 5), (x, y, -2.5), vol_resolution=1, stride=1) # quiver plot of (Bx, By, Bz) in 3 dimensions
	plot_3d_fields3(volume, (box, box, 5), (x, y, -2.5), vol_resolution=1, stride=1, level=level) # Bz at z=0