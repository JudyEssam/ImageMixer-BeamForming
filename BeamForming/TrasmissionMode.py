
import numpy as np
import matplotlib.pyplot as plt
from BeamSimulator import BeamForming

class TransmissionMode:
    def __init__(self,parent):
        self.parent=parent
        self.array=None
        self.signal=None

    def use_array_and_signal(self, array, signal):
        self.array = array  
        self.signal = signal

    def run_mode(self):
        wavelength= self.signal.get_wavelength()
        #form steer_vector
        self.array.form_steer_vector(wavelength, 'T')
        #apply signal to array (steer vector)
        self.beamforming= BeamForming(self.array, self.signal)
        #draw beam pattern
        self.beamforming.find_beam_pattern( self.parent.beam_pattern_widget)
        #draw interference map
        self.beamforming.find_interference_map(self.parent.interference_map_widget)   
        