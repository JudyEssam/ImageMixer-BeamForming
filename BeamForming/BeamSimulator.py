import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QVBoxLayout


class BeamForming:
    def __init__(self, array, signal):
        self._signal= signal
        self._array=array
        self._resulted_signal=None
    
    def apply_signal_to_array(self, mode):
        signal=self._signal.get_signal_data()
        steer_vector = self._array.get_steer_vector()
        steer_vector = steer_vector.reshape(-1,1) # make s a column vector nx1
        signal = signal.reshape(1,-1) # make signal a row vector 1 X no_of_sampling points
        #each row correspond to the signal recieved/transmitted by one element in the array
        self._resulted_signal= steer_vector @ signal #shape= no_of_elements*no_of_samples
        #apply noise to the signal if recieved
        if mode== 'R':
            noise = np.random.randn( self._resulted_signal.shape) + 1j*np.random.randn(self._resulted_signal.shape)
            self._resulted_signal=  self._resulted_signal + 0.5*noise 

        return self._resulted_signal
    

    def find_beam_pattern(self, parent_widget):
        N_fft= 512 #number of points used in the fft
        elements_num=self._array.get_antennas_num()
        steer_vector = np.conj(self._array.get_steer_vector()) # or else our answer will be negative/inverted
        steer_vector_padded = np.concatenate((steer_vector, np.zeros(N_fft - elements_num ))) # zero pad to N_fft elements to get more resolution in the FFT
        steer_vector_fft_dB = 10*np.log10(np.abs(np.fft.fftshift(np.fft.fft(steer_vector_padded)))**2) # magnitude of fft in dB
        steer_vector_fft_dB -= np.max(steer_vector_fft_dB) # normalize to 0 dB at peak

        # Map the FFT bins to angles in radians
        theta_bins = np.linspace(-1*np.pi/2, np.pi/2, N_fft) # in radians

        # find max so we can add it to plot
        theta_max = theta_bins[np.argmax(steer_vector_fft_dB)]

        fig = Figure(figsize=(5, 5))
        ax = fig.add_subplot(111, projection='polar')
        ax.plot(theta_bins, steer_vector_fft_dB)  # Plot beam pattern
        ax.plot([theta_max], [np.max(steer_vector_fft_dB)], 'ro')  # Mark peak
        ax.text(theta_max, np.max(steer_vector_fft_dB) - 4, 
                f"{np.round(theta_max * 180 / np.pi)}°")  # Annotate peak in degrees
        
        ax.set_theta_zero_location('N') # make 0 degrees point up
        ax.set_theta_direction(-1) # increase anticlockwise
        # ax.set_rlabel_position(55)  # Move grid labels away from other labels
        ax.set_thetamin(-90) # only show top half
        ax.set_thetamax(90)
        ax.set_ylim([-50, 1])
        ax.set_title("Beam Pattern", va='bottom')

        # Embed plot into the PyQt widget
        canvas = FigureCanvas(fig)
        if parent_widget.layout() is None:
            layout = QVBoxLayout(parent_widget)  # Use the provided parent widget
            parent_widget.setLayout(layout)
        else:
            layout=parent_widget.layout()
            # Remove all existing widgets from the layout
            while layout.count() > 0:
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
        layout.addWidget(canvas)


    # def find_interference_map(self, parent_widget):
    #     k= self._signal.get_wavenumber()
    #     print(k)
    #     elements_phase, elements_gain = self._array.get_elements_phases_gains()
        
    #     azimuth_points = 200  # Number of azimuth points
    #     range_points = 200  # Number of radial distance points
    #     azimuth = np.linspace(-1*np.pi/2, np.pi/2, azimuth_points)
    #     distances = np.linspace(0.1, 50, range_points)  # Distance range (0.1 to 10 meters)


    #     #Get array properties
    #     antennas_num, spacing, _ = self._array.get_array_factor()
    #     positions = spacing * np.arange(antennas_num)  # Antenna positions along the array
    #     shift= (positions[-1]-positions[0])/2
    #     positions= shift- positions
        
    #     # Precompute polar coordinates
    #     azimuth_grid, radius_grid = np.meshgrid(azimuth, distances, indexing='ij')

    #     # Cartesian coordinates of grid points
    #     x_grid = radius_grid * np.cos(azimuth_grid)
    #     y_grid = radius_grid * np.sin(azimuth_grid)

    #     # Compute distances from all antennas to all grid points
    #     field_map = np.zeros((azimuth_points, range_points), dtype=complex)

    #     for i, element_pos in enumerate(positions):
    #         dx = x_grid - element_pos
    #         dy = y_grid
    #         distance_to_point = np.sqrt(dx**2 + dy**2)
            
    #         # Compute field contribution
    #         phase_shift = -1j * k * distance_to_point + elements_phase[i]  # Phase due to propagation (intrinsic and extrinsic)
    #         amplitude = elements_gain[i]   # Gain and distance-based attenuation
    #         field_map += amplitude * np.exp(phase_shift)            
            

    #     # Compute normalized intensity (magnitude squared)
    #     intensity_map = np.abs(field_map) ** 2
    #     intensity_map = intensity_map/ np.max(intensity_map)
        
    #     # Create polar plot
    #     fig = Figure(figsize=(5, 5))
    #     ax = fig.add_subplot(111, polar=True)

    #     # Plot the interference map
    #     im = ax.pcolormesh(azimuth, distances, intensity_map.T, shading='auto', cmap='viridis')
    #     r = np.abs(positions)  
    #     theta = np.where(positions >= 0, np.pi/-2, np.pi/2)  

    #     # Plot the antenna positions on the polar plot
    #     ax.plot(theta, r, 'bo')  
    #     ax.set_theta_zero_location('N') # make 0 degrees point up
    #     ax.set_theta_direction(-1) # increase clockwise
    #     ax.set_thetamin(-90) # only show top half
    #     ax.set_thetamax(90)
        
    #     ax.set_title("Interference Map", va='bottom')

    #     # Add colorbar
    #     fig.colorbar(im, ax=ax, label="Intensity")

    #     # Embed plot into the PyQt widget
    #     canvas = FigureCanvas(fig)
    #     if parent_widget.layout() is None:
    #         layout = QVBoxLayout(parent_widget)  # Use the provided parent widget
    #         parent_widget.setLayout(layout)
    #     else:
    #         layout=parent_widget.layout()
    #         # Remove all existing widgets from the layout
    #         while layout.count() > 0:
    #             item = layout.takeAt(0)
    #             widget = item.widget()
    #             if widget is not None:
    #                 widget.deleteLater()
    #     layout.addWidget(canvas)
    

    def find_interference_map(self, parent_widget):
        k = self._signal.get_wavenumber()
        print(k)
        elements_phase, elements_gain = self._array.get_elements_phases_gains()
        
        azimuth_points = 100  # Number of azimuth points
        range_points = 100  # Number of radial distance points


        # Get array properties
        antennas_num, spacing, _ = self._array.get_array_factor()
        positions = spacing * np.arange(antennas_num)  # Antenna positions along the array
        shift = (positions[-1] - positions[0]) / 2
        positions = shift - positions

        # Precompute Cartesian coordinates
        x_coords = np.linspace(-5, 5, range_points)  # X axis range
        y_coords = np.linspace(-5, 5, azimuth_points)  # Y axis range
        x_grid, y_grid = np.meshgrid(x_coords, y_coords, indexing='xy')

        # Compute distances from all antennas to all grid points
        field_map = np.zeros((y_coords.size, x_coords.size), dtype=complex)

        for i, element_pos in enumerate(positions):
            dx = x_grid - element_pos
            dy = y_grid
            distance_to_point = np.sqrt(dx**2 + dy**2)

            # Compute field contribution
            phase_shift = -1j * k * distance_to_point + elements_phase[i]  # Phase due to propagation
            amplitude = elements_gain[i]  # Gain and distance-based attenuation
            field_map += amplitude * np.exp(phase_shift)

        # Compute normalized intensity (magnitude squared)
        intensity_map = np.abs(field_map) ** 2
        intensity_map = intensity_map / np.max(intensity_map)

        # Create Cartesian plot
        fig = Figure(figsize=(6, 5))
        ax = fig.add_subplot(111)
        # Plot the interference map
        im = ax.pcolormesh(x_grid, y_grid, intensity_map, shading='auto', cmap='viridis')

        # Plot antenna positions
        ax.scatter(positions, np.zeros_like(positions), color='red', marker='o', label='Antennas')

        # Label and format the plot
        ax.set_title("Interference Map in Cartesian Coordinates")
        ax.set_xlabel("X Position (m)")
        ax.set_ylabel("Y Position (m)")
        ax.set_aspect('equal', adjustable='box')  # Keep correct proportions
        ax.legend()

        # Add colorbar
        fig.colorbar(im, ax=ax, label="Normalized Intensity")

        # Embed the plot into the parent widget
        canvas = FigureCanvas(fig)
        if parent_widget.layout() is None:
            layout = QVBoxLayout(parent_widget)
            parent_widget.setLayout(layout)
        else:
            layout = parent_widget.layout()
            # Clear the layout
            while layout.count() > 0:
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

        layout.addWidget(canvas)

    def plot_recieved_signal(self, parent_widget): #after delays and sum (conventional beamforming)
        fig = Figure(figsize=(6, 5))
        ax = fig.add_subplot(111)
        recieved_signal= self.apply_signal_to_array('R')
        for element_num in range(recieved_signal.shape[0]):
            ax.plot(np.asarray(recieved_signal[element_num,:]).squeeze().real[0:200])
        ax.legend()
        ax.set_title("Plot of first 200 samples of the signal recieved by each antenna")
        ax.set_xlabel("time")
        ax.set_ylabel("amplitude")
        # Embed the plot into the parent widget
        canvas = FigureCanvas(fig)
        if parent_widget.layout() is None:
            layout = QVBoxLayout(parent_widget)
            parent_widget.setLayout(layout)
        else:
            layout = parent_widget.layout()
            # Clear the layout
            while layout.count() > 0:
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

        layout.addWidget(canvas)
