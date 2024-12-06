import numpy as np
class Signal:
    def __init__(self, signal_frequency, sample_rate, number_sampling_points):
        self.signal_frequency= signal_frequency
        self.sample_rate= sample_rate
        self.number_sampling_points= number_sampling_points

    
    def create_tone(self):
        time = np.arange(self.number_sampling_points)/self.sample_rate 
        tone= np.exp(2j * np.pi * self.signal_frequency * time)
        return tone

