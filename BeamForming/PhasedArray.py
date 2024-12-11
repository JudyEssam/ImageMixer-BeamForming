import numpy as np
from PyQt5.QtWidgets import QSlider, QVBoxLayout
from PyQt5.QtCore import Qt


class PhasedArray:
    def __init__(self, antennas_num, antennas_spacing, shape, beam_angle, signal_wavelength=None, radius=None):
        self._antennas_num= antennas_num
        self._antennas_spacing= antennas_spacing
        self._shape=shape
        self._beam_angle= np.radians(beam_angle) #azimuth
        self._steer_vector=None
        self._signal_wavelength= signal_wavelength
        self._radius= radius #for circular shaped array
        self._antennas=[]
        self._elements_phase=[]
        self._elements_gain=[]
        self.sliders_gain=[]
        self.sliders_phase=[]


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
         self.form_steer_vector()
         return self._steer_vector
    def get_array_factor(self): #parameters of the array
         return self._antennas_num, self._antennas_spacing, self._beam_angle
    def get_antennas_num(self): #parameters of the array
         return self._antennas_num
    
    def visualize_array():
         pass
    
    def set_signal_wavelength(self,signal_wavelength):
         self._signal_wavelength= signal_wavelength
    
    def show_sliders_gain(self, elements_num, sliders_widget):
        gain_limits= (0,10)
        if sliders_widget.layout() is None:
            layout = QVBoxLayout(sliders_widget)
            sliders_widget.setLayout(layout)
        else:
            layout = sliders_widget.layout()
        for _ in range(elements_num):
            slider = QSlider(Qt.Vertical) 
            slider.setRange(gain_limits[0],gain_limits[1])  # Set slider range to control gain
            slider.setValue(5)
            layout.addWidget(slider)
            self.sliders_gain.append(slider)
        layout.setSpacing(30)

    def show_sliders_phase(self, elements_num, sliders_widget):
        phase_limits= (0,360)
        if sliders_widget.layout() is None:
            layout = QVBoxLayout(sliders_widget)
            sliders_widget.setLayout(layout)
        else:
            layout = sliders_widget.layout()
        for _ in range(elements_num):
            slider = QSlider(Qt.Vertical) 
            slider.setRange(phase_limits[0],phase_limits[1])  # Set slider range to control gain
            slider.setValue(180)
            layout.addWidget(slider)
            self.sliders_phase.append(slider)
        layout.setSpacing(30)
    
    def get_gain_sliders_vals(self):
         self.sliders_gain= [slider.value()/10 for slider in self.sliders_gain]
         return self.sliders_gain
    
    def get_phase_sliders_vals(self):
         self.sliders_phase= [np.radians(slider.value()) for slider in self.sliders_phase]
         return self.sliders_phase
    
    def set_elements_phases_and_gains(self, elements_phase, elements_gain):
        self._elements_phase=elements_phase
        self._elements_gain=elements_gain