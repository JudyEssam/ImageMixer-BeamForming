import numpy as np
import matplotlib.pyplot as plt


from abc import ABC

class BeamForming(ABC):
    def __init__(self, array, signal):
        self._signal= signal
        self._array=array
        self._resulted_signal=None
    
    def apply_signal_to_array(self, mode):
        signal=self._signal.create_tone()

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
    
    

    def find_beam_pattern(self):
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

        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
        ax.plot(theta_bins, steer_vector_fft_dB) # MAKE SURE TO USE RADIAN FOR POLAR
        ax.plot([theta_max], [np.max(steer_vector_fft_dB)],'ro')
        ax.text(theta_max - 0.1, np.max(steer_vector_fft_dB) - 4, np.round(theta_max * 180 / np.pi))
        ax.set_theta_zero_location('N') # make 0 degrees point up
        ax.set_theta_direction(-1) # increase clockwise
        ax.set_rlabel_position(55)  # Move grid labels away from other labels
        ax.set_thetamin(-90) # only show top half
        ax.set_thetamax(90)
        ax.set_ylim([-30, 1]) # because there's no noise, only go down 30 dB
        plt.show()

    


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
