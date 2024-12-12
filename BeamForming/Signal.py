import numpy as np
class Signal:

    def __init__(self, propagation_speed =3e8 ,sample_rate =1e4, number_sampling_points= 1e4):
        
        self.signal_frequency= []
        self.sample_rate= sample_rate
        self.number_sampling_points= number_sampling_points
        self.propagation_speed= propagation_speed
        self.signal_data=None

    def add_freq(self, freq):
        self.signal_frequency.append(freq* 10**6 )

    def create_signal(self, amp=1):
        self.calculate_wavenumber_wavelength()
        time = np.arange(self.number_sampling_points)/self.sample_rate 
        self.signal_data= amp * np.sum(
        [np.exp(2j * np.pi * freq * time) for freq in self.signal_frequency], axis=0)
        
    def calculate_wavenumber_wavelength(self):
        self.wavelength= self.propagation_speed/ np.average(self.signal_frequency)
        self.wave_number= 2 * np.pi / self.wavelength 

    def get_wavenumber(self):
        return self.wave_number
    
    def get_wavelength(self):
        return self.wavelength

    def get_signal_data(self):
        return self.signal_data
