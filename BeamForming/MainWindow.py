from PyQt5.QtWidgets import QMainWindow, QApplication,QPushButton,QListWidget, QDoubleSpinBox ,QSpinBox, QWidget, QLabel ,  QSlider, QRadioButton, QComboBox, QTableWidget, QTableWidgetItem, QCheckBox,QMenu,QTextEdit, QDialog, QFileDialog, QInputDialog, QSizePolicy,QScrollArea,QVBoxLayout,QHBoxLayout
from PyQt5.uic import loadUi
import sys
import os
from TrasmissionMode import TransmissionMode
from RecievingMode import RecievingMode
from PhasedArray import PhasedArray
from Antenna import Antenna
from Signal import Signal

class MainWindow1(QMainWindow):
    def __init__(self):
        super(MainWindow1, self).__init__()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        loadUi("../MainWindow.ui", self)

        self.phase_label = self.findChild(QLabel, "Phase_2")

        #add array button
        self.addArray = self.findChild(QPushButton, "add_array")
        self.addArray.setVisible(False)

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

        # Multi arrays check
        self.multi_array = self.findChild(QRadioButton, 'radioButton1_3')
        self.multi_array.toggled.connect(self.toggleBeamAngleMode)

        self.mode_combox= self.findChild(QComboBox, 'Mode_comboBox')
        self.mode_combox.currentIndexChanged.connect(self.selectMode)
        
        self.form_signal_button= self.findChild(QPushButton, 'apply')
        self.form_signal_button.clicked.connect(self.formSignal)
        self.form_signal_button.clicked.connect(self.formArray)
        self.form_signal_button.clicked.connect(self.formAntenna)
        
        #for array parameters
        self.spacing_spinbox=self.findChild(QDoubleSpinBox, 'elements_spacing')
        self.elements_num_spinbox=self.findChild(QSpinBox, 'elements_no')
        self.beam_angle_spinbox=self.findChild(QSpinBox, 'beam_angle')
        self.beam_angle_spinbox.setVisible(False)
        self.beamLabel = self.findChild(QLabel, "beam_label")
        self.beamLabel.setVisible(False)
        self.shape_combox= self.findChild(QComboBox, 'Shape_comboBox')
        self.shape_combox.currentIndexChanged.connect(self.updateLabelForShape)

       #for element parameters
        self.isotropic_checkbox= self.findChild(QCheckBox, 'Isotropic_checkbox')
        self.isotropic_checkbox.clicked.connect(self.check_isotropic) 
        self.phase_widget= self.findChild(QWidget, 'componList_2')
        self.gain_widget= self.findChild(QWidget, 'componList_3')

        #for signal parameters
        self.prop_speed_spinbox=self.findChild(QSpinBox, 'Speed_spinbox')
        self.freq_spinbox=self.findChild(QSpinBox, 'freqSpinBox')
        self.amplitude=self.findChild(QDoubleSpinBox, 'amplitude')
        self.add_freq_button=self.findChild(QPushButton, 'add_frequency')
        self.add_freq_button.clicked.connect(lambda : self.signal.add_freq(self.freq_spinbox.value()))

        #BEAM widgets
        self.beam_pattern_widget= self.findChild(QWidget, 'widget1')
        self.interference_map_widget= self.findChild(QWidget, 'widget2')
        
        self.mode=None
        self.array=None
        self.signal= Signal()


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
            self.loc_x.setVisible(False)
            self.loc_y.setVisible(False)
            self.spinbox_x.setVisible(False)
            self.spinbox_y.setVisible(False)

    def selectMode(self, index):
        if index==0:
            self.mode= TransmissionMode(self)
        elif index==1:
            self.beamLabel.setVisible(True)
            self.beam_angle_spinbox.setVisible(True)
            # self.mode= RecievingMode()

    def formArray(self):
        antennas_num= self.elements_num_spinbox.value()
        antennas_spacing=self.spacing_spinbox.value()
        beam_angle=self.beam_angle_spinbox.value()
        print("beam angle", type(beam_angle), beam_angle)
        shape= 'linear' if self.shape_combox.currentIndex()==1 else 'circular'
        self.array=PhasedArray(antennas_num, antennas_spacing, shape, beam_angle)
        self.array.show_sliders_phase(self.phase_widget)
    
    def check_isotropic(self):
        if self.isotropic_checkbox.isChecked():
            self.array.show_sliders_gain(self.gain_widget)


    def formAntenna(self):
        antennas_num = self.array.get_antennas_num()
        if self.isotropic_checkbox.isChecked():
            is_isotropic=True
            gains= [1]*antennas_num
        else:
            is_isotropic= False
            gains= self.array.get_gain_sliders_vals() 
        phases= self.array.get_phase_sliders_vals() 
        
        for idx in range(antennas_num):
            antenna=Antenna(is_isotropic=is_isotropic, phase= phases[idx], gain= gains[idx])
            self.array.add_antenna(antenna)
        self.array.set_elements_phases_and_gains(phases, gains)
    
    def formSignal(self):
        amplitude= self.amplitude.value()
        self.signal.create_signal(amplitude)
        self.mode.use_array_and_signal()
        self.mode.run_mode()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = MainWindow1()
    window.show()
    window.showMaximized()
    sys.exit(app.exec_())