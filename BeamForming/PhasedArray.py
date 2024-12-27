import numpy as np


class PhasedArray:
    def __init__(self, antennas_num, antennas_spacing, shape, beam_angle):
        self._antennas_num= antennas_num
        self._antennas_spacing= antennas_spacing/1000 #millimeters to meters
        self._shape=shape
        self._beam_angle= np.radians(beam_angle) #azimuth
        self._steer_vector=None
        self._radius= antennas_spacing #for circular shaped array, we take the radius instead of antennas_spacing
        self._antennas=[]
        self._elements_phase=[]
        self.geometry_phases=[]
        self._elements_gain=[]
        self.is_uniform_phase=True
        self.element_angles=None

    def add_antenna(self, antenna):
        self._antennas.append(antenna)

    def form_steer_vector(self, wavelength): #we simulate the array using a steering vector
        if self._shape == 'linear':
            # intrinsic phase shifts (due to element spacing) 
                spacing = self._antennas_spacing/wavelength
                self.geometry_phases = -1j* spacing * np.arange(self._antennas_num) * np.sin(self._beam_angle)          
        
        if self._shape == 'circular':
            # Compute the angular positions of each element on the circle
                self.element_angles = np.linspace(0, 2*np.pi, self._antennas_num, endpoint=False)
                self.geometry_phases = -1j * (2* np.pi/wavelength ) * self._radius * np.cos(self._beam_angle - self.element_angles)
                # radius = self._radius/wavelength # normalized by wavelength!
                # d = np.sqrt(2 * radius**2 * (1 - np.cos(2*np.pi/self._antennas_num)))
                # sf = 1.0 / (np.sqrt(2.0) * np.sqrt(1.0 - np.cos(2*np.pi/self._antennas_num))) # scaling factor based on geometry, eg for a hexagon it is 1.0
                # x = d * sf * np.cos(2 * np.pi / self._antennas_num * np.arange(self._antennas_num))
                # y = -1 * d * sf * np.sin(2 * np.pi / self._antennas_num * np.arange(self._antennas_num))
                # self._steer_vector = np.exp(1j * 2 * np.pi * (x * np.cos(self._beam_angle) + y * np.sin(self._beam_angle)))
        self._steer_vector = np.array(self._elements_gain)* np.exp(self.geometry_phases + 1j * np.array(self._elements_phase))

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
    
    def get_geometrical_phases(self):
         return self.geometry_phases
    
    def get_elements_angles(self):
         return self.element_angles
