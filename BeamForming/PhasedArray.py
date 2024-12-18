import numpy as np


class PhasedArray:
    def __init__(self, antennas_num, antennas_spacing, shape, beam_angle):
        self._antennas_num= antennas_num
        self._antennas_spacing= antennas_spacing #the normalized spacing (dm/lamda)
        self._shape=shape
        self._beam_angle= np.radians(beam_angle) #azimuth
        self._steer_vector=None
        self._radius= antennas_spacing #for circular shaped array, we take the radius instead of antennas_spacing
        self._antennas=[]
        self._elements_phase=[]
        self._elements_gain=[]
        self.is_uniform_phase=True
        self.element_angles=None

    def add_antenna(self, antenna):
        self._antennas.append(antenna)

    def form_steer_vector(self): #we simulate the array using a steering vector
        if self._shape == 'linear':
            # intrinsic phase shifts (due to element spacing) 
                geometry_phases = -2j * np.pi * self._antennas_spacing * np.arange(self._antennas_num) * np.sin(self._beam_angle)          
        
        if self._shape == 'circular':
            # Compute the angular positions of each element on the circle
                element_angles = np.linspace(0, 2 * np.pi, self._antennas_num, endpoint=False)
                geometry_phases = -2j * np.pi * (self._radius / self._signal_wavelength) * np.cos(element_angles - self._beam_angle)
        # Add individual phase offsets, account for individual gains 
        self._steer_vector = np.array(self._elements_gain)* np.exp(geometry_phases + 1j * np.array(self._elements_phase))
            


    def get_steer_vector(self):
        return self._steer_vector
    
    def get_array_factor(self): #parameters of the array
         return self._antennas_num, self._antennas_spacing, self._beam_angle
    
    def get_antennas_num(self): #parameters of the array
         return self._antennas_num
    
    def get_array_shape(self): #get array_shape
         return self._shape
    
    def get_circular_properties(self):
        return self._radius, self.element_angles
    
    def visualize_array():
         pass
    
    def set_uniform_phase(self, state):
        self.is_uniform_phase= state

    def set_elements_phases_and_gains(self, elements_phase, elements_gain):
        self._elements_phase=elements_phase
        self._elements_gain=elements_gain

    def calculate_beam_angle(array_position, reference_position):
        x_array, y_array = array_position
        x_ref, y_ref = reference_position
        return np.arctan2(y_array - y_ref, x_array - x_ref)  # Angle in radians

    def get_elements_phases_gains(self):
         return self._elements_phase, self._elements_gain
    

