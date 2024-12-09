import numpy as np
class Signal:
    def __init__(self, signal_frequency,  propagation_speed =3e8 ,sample_rate =1e4, number_sampling_points= 1e4):
        self.signal_frequency= signal_frequency
        self.sample_rate= sample_rate
        self.number_sampling_points= number_sampling_points
        self.propagation_speed= propagation_speed
        self.wavelength= self.propagation_speed/ self.signal_frequency
        self.wave_number= 2 * np.pi / self.wavelength 

    
    def create_tone(self, amp=1, phi=0):
        time = np.arange(self.number_sampling_points)/self.sample_rate 
        tone= amp* np.exp(2j * np.pi * self.signal_frequency * time + phi)
        return tone

    def get_wavenumber(self):
        return self.wave_number
    
    def get_wavelength(self):
        return self.wavelength

