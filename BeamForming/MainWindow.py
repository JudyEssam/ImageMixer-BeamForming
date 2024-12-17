from PyQt5.QtWidgets import QMainWindow, QApplication,QPushButton,QListWidget, QDoubleSpinBox ,QSpinBox, QWidget, QLabel ,  QSlider, QRadioButton, QComboBox, QTableWidget, QTableWidgetItem, QCheckBox,QMenu,QTextEdit, QDialog, QFileDialog, QInputDialog, QSizePolicy,QScrollArea,QVBoxLayout,QHBoxLayout
from PyQt5.uic import loadUi
import sys
import os
from PyQt5.QtCore import Qt
from TrasmissionMode import TransmissionMode
from RecievingMode import RecievingMode
from PhasedArray import PhasedArray
from Antenna import Antenna
from Signal import Signal
import numpy as np

class MainWindow1(QMainWindow):
    def __init__(self):
        super(MainWindow1, self).__init__()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        loadUi("../MainWindow.ui", self)

        self.label = self.findChild(QLabel, "label")
        self.label.setVisible(False)
        self.spinbox = self.findChild(QSpinBox, "spinBox")
        self.spinbox.setVisible(False)
       
        # Multi arrays check
        self.multi_array = self.findChild(QRadioButton, 'radioButton1_3')
        self.multi_array.toggled.connect(self.toggleBeamAngleMode)

        self.mode_combox= self.findChild(QComboBox, 'Mode_comboBox')
        self.mode_combox.currentIndexChanged.connect(self.selectMode)
        
        self.apply_button= self.findChild(QPushButton, 'apply')
        self.apply_button.clicked.connect(self.applyChanges)
       
        #for array parameters
        self.spacing_spinbox=self.findChild(QDoubleSpinBox, 'elements_spacing')
        self.elements_num_spinbox=self.findChild(QSpinBox, 'elements_no')
        self.beam_angle_spinbox=self.findChild(QSpinBox, 'beam_angle')
        self.shape_combox= self.findChild(QComboBox, 'Shape_comboBox')

        self.elements_num_spinbox.valueChanged.connect(self.showSliders)

       #for element parameters
        self.isotropic_checkbox= self.findChild(QCheckBox, 'Isotropic_checkbox')
        self.isotropic_checkbox.clicked.connect(self.check_isotropic) 
        self.phase_widget= self.findChild(QWidget, 'slidersWidget_phase')
        self.gain_widget= self.findChild(QWidget, 'slidersWidget_gain')

        self.sliders_phase=[]
        self.sliders_gain=[]
        #for signal parameters
        self.prop_speed_spinbox=self.findChild(QSpinBox, 'Speed_spinbox')
        self.freq_spinbox=self.findChild(QSpinBox, 'freqSpinBox')
        self.amp_spinbox=self.findChild(QDoubleSpinBox, 'amplitude')
        self.add_component_button=self.findChild(QPushButton, 'add_frequency')
        self.add_component_button.clicked.connect(lambda : self.signal.add_amp_freq(self.amp_spinbox.value(), self.freq_spinbox.value()))

        #BEAM widgets
        self.beam_pattern_widget= self.findChild(QWidget, 'widget1')
        self.interference_map_widget= self.findChild(QWidget, 'widget2')
        
        self.mode= TransmissionMode(self)
        self.array=None
        self.signal= Signal()

    def toggleBeamAngleMode(self, checked):
        """Toggle between Beam Angle and Location input."""
        if checked:
            # Change label text
            self.beam_label.setText("Location_x: ")
            self.label.setText("Location_y")
            self.label.setVisible(True)
            self.spinbox.setVisible(True)

        else:
            # Revert to Beam Angle mode
            self.beam_label.setText("Beam Angle: ")
            self.label.setVisible(False)
            self.spinbox.setVisible(False)

    def selectMode(self, index):
        if index==0:
            self.mode= TransmissionMode(self)
        elif index==1:
            self.mode= RecievingMode()

    def show_sliders_phase(self, sliders_widget, value):
        self.sliders_phase=[]
        phase_limits= (0,360)
        if sliders_widget.layout() is None:
            layout = QVBoxLayout(sliders_widget)
            sliders_widget.setLayout(layout)
        else:
            layout = sliders_widget.layout()
        for _ in range(value):
            slider = QSlider(Qt.Vertical) 
            slider.setRange(phase_limits[0],phase_limits[1])  # Set slider range to control gain
            slider.setValue(180)
            layout.addWidget(slider)
            self.sliders_phase.append(slider)
        layout.setSpacing(30)

    def show_sliders_gain(self, sliders_widget):
        self.sliders_gain=[]
        gain_limits= (0,10)
        if sliders_widget.layout() is None:
            layout = QVBoxLayout(sliders_widget)
            sliders_widget.setLayout(layout)
        else:
            layout = sliders_widget.layout()
        for _ in range(len(self.sliders_phase)):
            slider = QSlider(Qt.Vertical) 
            slider.setRange(gain_limits[0],gain_limits[1])  # Set slider range to control gain
            slider.setValue(5)
            layout.addWidget(slider)
            self.sliders_gain.append(slider)
        layout.setSpacing(30)
    
    def clear_sliders(self, sliders_widget):
        layout = sliders_widget.layout()
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
    
    def showSliders(self, value):
        self.clear_sliders(self.phase_widget)
        self.show_sliders_phase(self.phase_widget, value)
        self.check_isotropic()

    def check_isotropic(self):
        self.clear_sliders(self.gain_widget)
        if self.isotropic_checkbox.isChecked() == False: #not checked (tapered gain)
            self.show_sliders_gain(self.gain_widget)

    def get_gain_sliders_vals(self):
         self.sliders_gain_values= [slider.value()/10 for slider in self.sliders_gain]
         return self.sliders_gain_values
    
    def get_phase_sliders_vals(self):
         self.sliders_phase_values= [np.radians(slider.value()) for slider in self.sliders_phase]
         return self.sliders_phase_values

    def formArray(self):
        antennas_num= self.elements_num_spinbox.value()
        antennas_spacing=self.spacing_spinbox.value()
        beam_angle=self.beam_angle_spinbox.value()
        print("beam angle", type(beam_angle), beam_angle)
        shape= 'linear' if self.shape_combox.currentIndex()==0 else 'circular'
        self.array=PhasedArray(antennas_num, antennas_spacing, shape, beam_angle)    

    def formAntenna(self):
        antennas_num = self.array.get_antennas_num()
        if self.isotropic_checkbox.isChecked():
            is_isotropic=True
            gains= [1]*antennas_num
        else:
            is_isotropic= False
            gains= self.get_gain_sliders_vals() 
        phases= self.get_phase_sliders_vals() 
        
        for idx in range(antennas_num):
            antenna=Antenna(is_isotropic=is_isotropic, phase= phases[idx], gain= gains[idx])
            self.array.add_antenna(antenna)
        self.array.set_elements_phases_and_gains(phases, gains)
    
    def formSignal(self):
        self.signal.create_signal()
        
    def applyChanges(self):
        self.formArray()
        self.formAntenna()
        self.formSignal()
        self.mode.use_array_and_signal(self.array, self.signal)
        self.mode.run_mode()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow1()
    window.show()
    window.showMaximized()
    sys.exit(app.exec_())