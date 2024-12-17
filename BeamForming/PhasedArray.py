from PyQt5.QtWidgets import QSlider, QVBoxLayout
from PyQt5.QtCore import Qt
import numpy as np


class PhasedArray:
    def __init__(self, antennas_num, antennas_spacing, shape, beam_angle, radius=None):
        self._antennas_num= antennas_num
        self._antennas_spacing= antennas_spacing #the normalized spacing (dm/lamda)
        self._shape=shape
        self._beam_angle= np.radians(beam_angle) #azimuth
        self._steer_vector=None
        self._radius= radius #for circular shaped array
        self._antennas=[]
        self._elements_phase=[]
        self._elements_gain=[]
        self.sliders_gain=[]
        self.sliders_phase=[]
        self.phase_shift= None #for uniform phase shift, in radians
        self.is_uniform_phase=True


    def add_antenna(self, antenna):
        self._antennas.append(antenna)

    def form_steer_vector(self, signal_wavelength, mode,): #we simulate the array using a steering vector
        antennas_indices= np.arange(self._antennas_num)
        if self._shape == 'linear':
            # intrinsic phase shifts (due to element spacing) 
            
            if mode=='R': #for recieving mode, we know the direction of arrival (i.e. the beam angle)
                geometry_phases = -2j * np.pi * self._antennas_spacing * antennas_indices * np.sin(self._beam_angle)  
                # Add individual phase offsets, account for individual gains 
                self._steer_vector = np.array(self._elements_gain)* np.exp(geometry_phases + 1j * np.array(self._elements_phase))
           
            elif mode=='T': #for transmission mode, we get the direction of transmission (beam angle) using phase shift
                if self.is_uniform_phase:
                    sin_angle= (self.phase_shift)/(2*np.pi*self._antennas_spacing)
                    if 1 < sin_angle < -1: 
                        print("sine angle", sin_angle)
                        raise ValueError("Sine cannot exceed 1 or -1")
                    geometry_phases = -2j * np.pi * self._antennas_spacing * antennas_indices* sin_angle
                    self._steer_vector = np.array(self._elements_gain)* np.exp(geometry_phases)
                else:
                    raise ValueError("This Case is not handled yet")

        elif self._shape == 'circular':
            # Compute the angular positions of each antenna around the circle
            element_angles = np.linspace(0, 2 * np.pi, self._antennas_num, endpoint=False)

            if mode == 'R':
                # Receiving mode: Known direction of arrival (DOA)
                geometry_phases = -2j * np.pi * (self._radius / signal_wavelength) * np.cos(element_angles - self._beam_angle)
                self._steer_vector = np.array(self._elements_gain)* np.exp(geometry_phases + 1j * np.array(self._elements_phase))

            elif mode == 'T':
                # Transmission mode: Phase shifts determine beam direction
                if self.is_uniform_phase:
                    # Use phase shift between adjacent elements to steer the beam
                    cumulative_phase_shifts = self.phase_shift * np.arange(self._antennas_num)
                    geometry_phases = -2j * np.pi * (self._radius / signal_wavelength) * np.cos(element_angles) + 1j * cumulative_phase_shifts
                    
                    self._steer_vector = np.array(self._elements_gain) * np.exp(geometry_phases)
                else:
                    raise ValueError("Non-uniform phase case not yet handled")
            


    def get_steer_vector(self):
        return self._steer_vector
    
    def get_array_factor(self): #parameters of the array
         return self._antennas_num, self._antennas_spacing, self._beam_angle
    def get_antennas_num(self): #parameters of the array
         return self._antennas_num
    
    def visualize_array():
         pass
    
    
    def set_elements_phases_and_gains(self, elements_phase, elements_gain):
        self._elements_phase=elements_phase
        self._elements_gain=elements_gain

    def calculate_beam_angle(array_position, reference_position):
        x_array, y_array = array_position
        x_ref, y_ref = reference_position
        return np.arctan2(y_array - y_ref, x_array - x_ref)  # Angle in radians

    def get_elements_phases_gains(self):
         return self._elements_phase, self._elements_gain