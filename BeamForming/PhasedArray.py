import numpy as np

class PhasedArray:
    def __init__(self, antennas_num, antennas_spacing,beam_angle, shape, signal_wavelength, radius=None):
        self._antennas_num= antennas_num
        self._antennas_spacing= antennas_spacing
        self._shape=shape
        self._beam_angle= np.radians(beam_angle) #azimuth
        self._steer_vector=None
        self._signal_wavelength= signal_wavelength
        self._radius= radius #for circular shaped array
        self._antennas=[]
        self._element_phases=[]
        self._element_gain=[]


    def add_antenna(self, antenna):
        self._antennas.append(antenna)
        self._element_phases.append(antenna.phase)
        self._element_gain.append(antenna.gain)

    def form_steer_vector(self): #we simulate the array using a steering vector
        if self._shape == 'linear':
            # intrinsic phase shifts (due to element spacing) 
                geometry_phases = -2j * np.pi * self._antennas_spacing * np.arange(self._antennas_num) * np.sin(self._beam_angle)       
        if self._shape == 'circular':
            # Compute the angular positions of each element on the circle
                element_angles = np.linspace(0, 2 * np.pi, self._antennas_num, endpoint=False)
                geometry_phases = -2j * np.pi * (self._radius / self._signal_wavelength) * np.cos(element_angles - self._beam_angle)
        # Add individual phase offsets, account for individual gains 
        self._steer_vector = np.array(self._element_gain)* np.exp(geometry_phases + 1j * np.array(self._element_phases))

    def get_steer_vector(self):
         return self._steer_vector
    def get_array_factor(self): #parameters of the array
         return self._antennas_num, self._antennas_spacing, self._beam_angle
    
    def visualize_array():
         pass