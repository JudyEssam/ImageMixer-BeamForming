import numpy as np
from BeamSimulator import BeamForming
from PhasedArray import PhasedArray
class RecievingMode:

    def __init__(self, parent):
        self.parent=parent
        self.array=None
        self.signal=None


    def use_array_and_signal(self, array, signal):
        self.array = array  # Always access the updated parent attributes
        self.signal = signal

    # def transmission_towers(self):
    #     sending_towers= PhasedArray(2, 0.5, 'linear', 30)
    #     return sending_towers


    def run_mode(self):
        wavelength= self.signal.get_wavelength()
        #form steer_vector
        self.array.form_steer_vector(wavelength)
        #apply signal to array (steer vector)
        self.beamforming= BeamForming(self.array, self.signal)
        #draw beam pattern
        self.beamforming.find_beam_pattern( self.parent.beam_pattern_widget, self.array.get_array_shape())
        #plot towers transmssion map
        self.beamforming.plot_towers_interference_map(self.parent.interference_map_widget)
