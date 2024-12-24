import numpy as np
class Signal:

    def __init__(self, propagation_speed =3e8 ,sample_rate =1e4, number_sampling_points= 1e4):
        
        self.signal_frequency= []
        self.amp=[]
        self.sample_rate= sample_rate
        self.number_sampling_points= number_sampling_points
        self.propagation_speed= propagation_speed
        self.signal_data=None
        self.wave_number=None

    def add_freq(self, freq):
        self.signal_frequency.append(freq)
    

    # def create_signal(self):
    #     self.calculate_wavenumber_wavelength()
    #     time = np.arange(self.number_sampling_points)/self.sample_rate 
    #     self.signal_data= np.sum([self.amp[i] *np.exp(2j * np.pi * self.signal_frequency[i] * time) for i in range(len(self.amp))], axis=0)

    def create_signal(self):
        self.calculate_wavenumber_wavelength()
        x = np.linspace(-5, 5, 1000)  # Spatial positions from 0 to 10 meters
        t = np.arange(0, 1, 0.001)   # Time from 0 to 1 second in 0.01s steps
        X, T = np.meshgrid(x, t)    # Create a grid of (x, t) pairs 
        self.signal_data = np.sum([
        self.amp[i] * np.exp(1j * (self.wave_number[i] * X - 2 * np.pi * self.signal_frequency[i] * T))
        for i in range(len(self.amp))], axis=0)
        

    def calculate_wavenumber_wavelength(self):
        self.wavelength = [self.propagation_speed / f for f in self.signal_frequency]
        self.wave_number = [2 * np.pi / wl for wl in self.wavelength]
    
    def set_speed(self,propagation_speed):
         self.propagation_speed= propagation_speed

    def get_wavenumber(self):
        return self.wave_number[0]
    
    def get_wavelength(self):
        return self.wavelength[0]

    def get_signal_data(self):
        return self.signal_data
