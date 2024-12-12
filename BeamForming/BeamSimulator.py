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
        theta_bins = np.arcsin(np.linspace(-1, 1, N_fft)) # in radians

        # find max so we can add it to plot
        theta_max = theta_bins[np.argmax(steer_vector_fft_dB)]

        fig = Figure()
        ax = fig.add_subplot(111, projection='polar')
        ax.plot(theta_bins, steer_vector_fft_dB)  # Plot beam pattern
        ax.plot([theta_max], [np.max(steer_vector_fft_dB)], 'ro')  # Mark peak
        ax.text(theta_max - 0.1, np.max(steer_vector_fft_dB) - 4, 
                f"{np.round(theta_max * 180 / np.pi)}°")  # Annotate peak in degrees
        ax.set_theta_zero_location('N')  # Set 0 degrees pointing up
        ax.set_theta_direction(-1)  # Clockwise angle increase
        ax.set_rlabel_position(55)  # Adjust radial grid labels
        ax.set_thetamin(-90)  # Show only top half
        ax.set_thetamax(90)
        ax.set_ylim([-30, 1])  # Limit radial axis to -30 dB minimum

        # Embed plot into the PyQt widget
        canvas = FigureCanvas(fig)
        layout = QVBoxLayout(parent_widget)  # Use the provided parent widget
        layout.addWidget(canvas)
        parent_widget.setLayout(layout)

    def find_DOA(self): #for Receiving mode only- Get Direction of arrival (we don't know the beam angle)
        recieved_signal= self.apply_signal_to_array('R')
        elements_num,spacing,_= self._array.get_array_factor()
        theta_scan = np.linspace(-1*np.pi, np.pi, 1000) # 1000 different thetas between -180 and +180 degrees
        results = []
        #These weights align the phases of incoming signals from different directions.
        for theta_i in theta_scan:
            weights = np.exp(-2j * np.pi * spacing * np.arange(elements_num) * np.sin(theta_i)) # Conventional, aka delay-and-sum, beamformer
            X_weighted = weights.conj().T @ recieved_signal # apply our weights. (i.e., perform the beamforming)
            results.append(10*np.log10(np.var(X_weighted))) # power in signal, in dB so its easier to see small and large lobes at the same time
        results -= np.max(results) # normalize (optional)

        # print angle that gave us the max value
        print(theta_scan[np.argmax(results)] * 180 / np.pi) 
       
        #Graphing DOA
        # plt.plot(theta_scan*180/np.pi, results) # lets plot angle in degrees
        # plt.xlabel("Theta [Degrees]")
        # plt.ylabel("DOA Metric")
        # plt.grid()
        # plt.show()
    
    def find_interference_map(self, parent_widget):
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
        fig = Figure(figsize=(8, 8))
        ax = fig.add_subplot(111, polar=True)

        # Plot the interference map
        im = ax.pcolormesh(azimuth, distances, intensity_map, shading='auto', cmap='viridis')
        r = np.abs(positions)  
        theta = np.where(positions >= 0, 0, np.pi)  

        # Plot the antenna positions on the polar plot
        ax.plot(theta, r, 'bo')  
        ax.set_theta_zero_location("E")  # Set the top as 0 degrees
        ax.set_theta_direction(1)  # antiClockwise azimuth
        ax.set_title("Interference Map", va='bottom')

        # Add colorbar
        fig.colorbar(im, ax=ax, label="Intensity")

        # Embed plot into the PyQt widget
        canvas = FigureCanvas(fig)
        layout = QVBoxLayout(parent_widget)  # Use the provided parent widget
        layout.addWidget(canvas)
        parent_widget.setLayout(layout)
    


# if __name__ =='__main__':
#     array = PhasedArray(
#     antennas_num=8,
#     antennas_spacing=0.5,
#     beam_angle=30,
#     shape='linear',
#     signal_wavelength=0.03
#     )
#     array.form_steer_vector()
#     signal_frequency = 1468  # 1 GHz
#     signal= Signal(signal_frequency)

#     # Parameters
#     grid_size = (500, 500)  # Resolution of the grid
#     grid_range = ((-np.pi / 2, np.pi / 2), (0, 10))  # Azimuth (-90 to +90 degrees), distance (0 to 10 meters)
    
#     beamformer= BeamForming(array,signal)
#     #beamformer.find_beam_pattern()
#     # Compute and plot the interference map
#     beamformer.find_interference_map()
#     result= beamformer.apply_signal_to_array('T')
#     #plt.plot(result)
