import numpy as np
class Signal:
    def __init__(self, signal_frequency, sample_rate =1e6, number_sampling_points= 10000):
        self.signal_frequency= signal_frequency
        self.sample_rate= sample_rate
        self.number_sampling_points= number_sampling_points
        self.propagation_speed= 3e8
        self.wavelength= self.propagation_speed/ self.signal_frequency
        self.wave_number= 2 * np.pi / self.wavelength 

    
    def create_tone(self):
        time = np.arange(self.number_sampling_points)/self.sample_rate 
        tone= np.exp(2j * np.pi * self.signal_frequency * time)
        return tone

    def get_wavenumber(self):
        return self.wave_number
    
    def get_wavelength(self):
        return self.wavelength

