
from BeamSimulator import BeamForming
import numpy as np
import matplotlib.pyplot as plt


class TransmissionMode(BeamForming):
    def __init__(self):
        super().__init__(self)
 
    def find_interference_map(self):
        k= self._signal.get_wavenumber()
        print(k)
        
        azimuth_points = 500  # Number of azimuth points
        range_points = 500  # Number of radial distance points
        azimuth = np.linspace(0, 2*np.pi, azimuth_points)
        distances = np.linspace(0.1, 10, range_points)  # Distance range (0.1 to 10 meters)


        #Get array properties
        antennas_num, spacing, _ = self._array.get_array_factor()
        positions = spacing * np.arange(antennas_num)  # Antenna positions along the array
        shift= (positions[-1]-positions[0])/2
        positions= shift- positions
        
        # Precompute polar coordinates
        azimuth_grid, radius_grid = np.meshgrid(azimuth, distances, indexing='ij')

        # Cartesian coordinates of grid points
        x_grid = radius_grid * np.cos(azimuth_grid)
        y_grid = radius_grid * np.sin(azimuth_grid)

        # Compute distances from all antennas to all grid points
        field_map = np.zeros((azimuth_points, range_points), dtype=complex)

        for element_pos in positions:
            dx = x_grid - element_pos
            dy = y_grid
            distance_to_point = np.sqrt(dx**2 + dy**2)
            
            # Compute field contribution
            phase_shift = -1j * k * distance_to_point  # Phase due to propagation
            amplitude = 1   # Gain and distance-based attenuation
            field_map += amplitude * np.exp(phase_shift)            
            

        # Compute normalized intensity (magnitude squared)
        intensity_map = np.abs(field_map) ** 2
        #intensity_map /= np.max(intensity_map)  # Normalize

        # Create polar plot
        plt.figure(figsize=(8, 8))
        ax = plt.subplot(111, polar=True)
        #ax.plot(azimuth_grid,radius_grid)

        # Plot the interference map
        im = ax.pcolormesh(azimuth, distances, intensity_map, shading='auto', cmap='viridis')  # Transpose for pcolormesh
        plt.colorbar(im, ax=ax, label="Intensity")
        r = np.abs(positions)  
        theta = np.where(positions >= 0, 0, np.pi)  
        # Plot the antenna positions on the polar plot
        ax.plot(theta, r, 'bo')  
        ax.set_theta_zero_location("E")  # Set the top as 0 degrees
        ax.set_theta_direction(1)  # antiClockwise azimuth
        ax.set_title("Interference Map",  va='bottom')
        plt.show()
