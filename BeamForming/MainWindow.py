from PyQt5.QtWidgets import QMainWindow, QApplication,QPushButton, QListWidget, QDoubleSpinBox ,QSpinBox, QWidget, QLabel ,  QSlider, QRadioButton, QComboBox, QTableWidget, QTableWidgetItem, QCheckBox,QMenu,QTextEdit, QDialog, QFileDialog, QInputDialog, QSizePolicy,QScrollArea,QVBoxLayout,QHBoxLayout
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
from Scenarios import Scenarios

class MainWindow1(QMainWindow):
    def __init__(self):
        super(MainWindow1, self).__init__()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        loadUi("../MainWindow.ui", self)

        self.phase_label = self.findChild(QLabel, "Phase_2")

        #interference map label
        self.interfere_label = self.findChild(QLabel ,"label_4")

        #add array button
        self.addArray = self.findChild(QPushButton, "add_array")
        self.addArray.setVisible(False)

        #scenarios
        self.scenarios_comboBox= self.findChild(QComboBox, 'scenarios_comboBox')
        self.scenarios_comboBox.activated.connect(self.choose_scenario)

        #for x and y location
        self.loc_x = self.findChild(QLabel, "locX")
        self.loc_x.setVisible(False)
        self.spinbox_x = self.findChild(QSpinBox, "spinBox_X")
        self.spinbox_x.setVisible(False)

        self.loc_y = self.findChild(QLabel, "locY")
        self.loc_y.setVisible(False)
        self.spinbox_y = self.findChild(QSpinBox, "spinBox_Y")
        self.spinbox_y.setVisible(False)

        # Multi arrays check
        self.multi_array = self.findChild(QRadioButton, 'radioButton1_3')
        self.multi_array.toggled.connect(self.toggleBeamAngleMode)

        #Mode
        self.mode_combox= self.findChild(QComboBox, 'Mode_comboBox')
        self.mode_combox.activated.connect(self.selectMode)
        
       
        #for array parameters
        self.spacing_spinbox=self.findChild(QDoubleSpinBox, 'elements_spacing')
        self.elements_num_spinbox=self.findChild(QSpinBox, 'elements_no')

        self.beamAngle = self.findChild(QSlider, "beam_angle")
        self.beamAngle.valueChanged.connect(self.get_beam_angle_value)
        self.slider_value = self.findChild(QLabel, "label")

        self.beamLabel = self.findChild(QLabel, "beam_label")
        self.beamLabel.setText("Steering Angle: ")
        self.shape_combox= self.findChild(QComboBox, 'Shape_comboBox')
        self.shape_combox.currentIndexChanged.connect(self.updateLabelForShape)

        self.elements_num_spinbox.valueChanged.connect(self.showSliders)

       #for element parameters
        self.isotropic_checkbox= self.findChild(QCheckBox, 'Isotropic_checkbox')
        self.isotropic_checkbox.clicked.connect(self.check_isotropic)
        self.uniform_phase_checkbox= self.findChild(QCheckBox, 'checkBox')
        self.uniform_phase_checkbox.clicked.connect(self.check_uniform_phase) 
        self.phase_widget= self.findChild(QWidget, 'slidersWidget_phase')
        self.gain_widget= self.findChild(QWidget, 'slidersWidget_gain')

        self.sliders_phase=[]
        self.sliders_gain=[]
        
        #for signal parameters
        self.freq_spinbox=self.findChild(QSpinBox, 'freqSpinBox')
        self.freq_comboBox = self.findChild(QComboBox, 'freq_comboBox')
        self.freq_comboBox.setCurrentIndex(0)
        self.freq_comboBox.activated.connect(self.get_frequency_multiplier)

        self.add_component_button=self.findChild(QPushButton, 'add_frequency')
        self.add_component_button.clicked.connect(lambda : self.signal.add_freq( self.freq_spinbox.value() * 10 ** self.get_frequency_multiplier()))

        #propagation speed
        self.speed_comboBox = self.findChild(QComboBox, 'speed_comboBox')
        self.speed_comboBox.setCurrentIndex(0)
        self.speed_comboBox.activated.connect(self.update_speed)

        #BEAM widgets
        self.beam_pattern_widget= self.findChild(QWidget, 'widget1')
        self.interference_map_widget= self.findChild(QWidget, 'widget2')
        
        self.mode= TransmissionMode(self)
        self.array=None
        self.signal= Signal()
        self.scenario= Scenarios(self)
        self.scenario.ultrasonic()
        self.setup_auto_apply()

    def setup_auto_apply(self):
        """Connect signals to call applyChanges when components are updated."""
        self.scenarios_comboBox.activated.connect(self.applyChanges)
        self.mode_combox.activated.connect(self.applyChanges)
        self.spacing_spinbox.valueChanged.connect(self.applyChanges)
        self.elements_num_spinbox.valueChanged.connect(self.applyChanges)
        self.beamAngle.valueChanged.connect(self.applyChanges)
        self.shape_combox.currentIndexChanged.connect(self.applyChanges)
        self.isotropic_checkbox.clicked.connect(self.applyChanges)
        self.uniform_phase_checkbox.clicked.connect(self.applyChanges)
        self.freq_spinbox.valueChanged.connect(self.applyChanges)
        self.freq_comboBox.activated.connect(self.applyChanges)
        self.speed_comboBox.activated.connect(self.applyChanges)
        self.multi_array.toggled.connect(self.applyChanges)

    def get_frequency_multiplier(self):
        index = self.freq_comboBox.currentIndex()
        if index == 0:  # Hz
            return 0
        elif index == 1:  # kHz
            return 3
        elif index == 2:  # MHz
            return 6
        elif index == 3:  # GHz
            return 9

    def update_speed(self, index=None):
        if index is None:
            index = self.speed_comboBox.currentIndex()  # Use the current index of the combo box
        if index == 0:  # Light speed
            return 3 * 10**8
        elif index == 1:  # Ultrasound speed
            return 1540


    def choose_scenario(self, index):
        if index == 0:
            self.scenario.ultrasonic()
        elif index==1:
            self.scenario.beamforming_5G()
        elif index==2:
            self.scenario.ablation()
        elif index==3:
            self.scenario.default()


    def updateLabelForShape(self, index):
        if index == 1:  # "Circular" is the second item (index 1)
            self.phase_label.setText("Radius: ")
        else:  # Default to "Linear" (index 0)
            self.phase_label.setText("Element Spacing: ")     

    def toggleBeamAngleMode(self, checked):
        """Toggle between Beam Angle and Location input."""
        if checked:
            # Change label text
            self.addArray.setVisible(True)
            self.loc_x.setVisible(True)
            self.loc_y.setVisible(True)
            self.spinbox_x.setVisible(True)
            self.spinbox_y.setVisible(True)

        else:
            # Revert to Beam Angle mode
            self.addArray.setVisible(False)
            self.loc_x.setVisible(False)
            self.loc_y.setVisible(False)
            self.spinbox_x.setVisible(False)
            self.spinbox_y.setVisible(False)

    def selectMode(self, index):
        if index==0:
            self.mode= TransmissionMode(self)
            self.beamLabel.setText("Steering Angle: ")
            self.interfere_label.setText("Interference Map")
        elif index==1:
            self.interfere_label.setText("Tower Transmission Map")
            self.mode= RecievingMode(self)
            self.beamLabel.setText("Direction of Arrival: ")

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
            slider.valueChanged.connect(self.applyChanges)
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

    def show_sliders_phase(self, sliders_widget):
        self.sliders_phase = []
        phase_limits = (0, 360)
        if sliders_widget.layout() is None:
            layout = QVBoxLayout(sliders_widget)
            sliders_widget.setLayout(layout)
        else:
            layout = sliders_widget.layout()
        for _ in range(self.elements_num_spinbox.value()):
            slider = QSlider(Qt.Vertical)
            slider.setRange(phase_limits[0], phase_limits[1])  # Set slider range
            slider.setValue(180)
            slider.valueChanged.connect(self.applyChanges)  # Connect to applyChanges
            layout.addWidget(slider)
            self.sliders_phase.append(slider)
        layout.setSpacing(30)


    def show_sliders_gain(self, sliders_widget):
        self.sliders_gain = []
        gain_limits = (0, 10)
        if sliders_widget.layout() is None:
            layout = QVBoxLayout(sliders_widget)
            sliders_widget.setLayout(layout)
        else:
            layout = sliders_widget.layout()
        for _ in range(self.elements_num_spinbox.value()):
            slider = QSlider(Qt.Vertical)
            slider.setRange(gain_limits[0], gain_limits[1])  # Set slider range
            slider.setValue(5)
            slider.valueChanged.connect(self.applyChanges)  # Connect to applyChanges
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
        self.check_uniform_phase()
        self.check_isotropic()

    def check_uniform_phase(self, ):
        self.clear_sliders(self.phase_widget)
        if self.uniform_phase_checkbox.isChecked()==False: 
            self.show_sliders_phase(self.phase_widget)
       

    def check_isotropic(self,):
        self.clear_sliders(self.gain_widget)
        if self.isotropic_checkbox.isChecked() == False: #not checked (tapered gain)
            self.show_sliders_gain(self.gain_widget, )

    def get_gain_sliders_vals(self):
         self.sliders_gain_values= [slider.value()/10 for slider in self.sliders_gain]
         return self.sliders_gain_values
    
    def get_phase_sliders_vals(self):
         self.sliders_phase_values= [np.radians(slider.value()) for slider in self.sliders_phase]
         return self.sliders_phase_values


    def get_beam_angle_value(self):
        value = self.beamAngle.value()
        self.slider_value.setText(f"Value: {value}")
        return value

    def formArray(self):
        antennas_num= self.elements_num_spinbox.value()
        antennas_spacing=self.spacing_spinbox.value() #acts as radius for circular array
        print(f"antennas_spacing{antennas_spacing}")
        beam_angle=self.get_beam_angle_value()
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
        if self.uniform_phase_checkbox.isChecked():
            phases= [0] * antennas_num
            self.array.set_uniform_phase(True)
        else:
            phases=self.get_phase_sliders_vals()
            self.array.set_uniform_phase(False)
        
        for idx in range(antennas_num):
            antenna=Antenna(is_isotropic=is_isotropic, phase= phases[idx], gain= gains[idx])
            self.array.add_antenna(antenna)
        self.array.set_elements_phases_and_gains(phases, gains)
    
    def formSignal(self):
        self.signal.renew_amp_freq(self.freq_spinbox.value() * 10 ** self.get_frequency_multiplier())
        current_index = self.speed_comboBox.currentIndex()  
        self.signal.set_speed(self.update_speed(current_index))
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