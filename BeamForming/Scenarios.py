class Scenarios:
    def __init__(self, parent):
        self.parent= parent
        self.parent.elements_num_spinbox.setValue(8)
        self.parent.spacing_spinbox.setValue(0.5)
        self.parent.beamAngle.setValue(20)
        self.parent.isotropic_checkbox.setChecked(True)
        self.parent.checkBox.setChecked(True)
        self.parent.speed_comboBox.setCurrentIndex(1)
        self.parent.freq_spinbox.setValue(10)
        self.parent.freq_comboBox.setCurrentIndex(2)
        

    def ultrasonic(self):
        self.parent.mode_combox.setCurrentIndex(0)
        self.parent.selectMode(0)
        self.parent.elements_num_spinbox.setValue(8)
        self.parent.spacing_spinbox.setValue(0.5)
        self.parent.beamAngle.setValue(20)
        self.parent.isotropic_checkbox.setChecked(True)
        self.parent.checkBox.setChecked(True)
        self.parent.speed_comboBox.setCurrentIndex(1)
        self.parent.check_isotropic()
        self.parent.check_uniform_phase()


    def beamforming_5G(self):
        self.parent.elements_num_spinbox.setValue(8)
        self.parent.spacing_spinbox.setValue(0.5)
        self.parent.beamAngle.setValue(20)
        self.parent.isotropic_checkbox.setChecked(True)
        self.parent.checkBox.setChecked(True)
        self.parent.speed_comboBox.setCurrentIndex(0)
        self.parent.freq_spinbox.setValue(2)
        self.parent.freq_comboBox.setCurrentIndex(3)       
        self.parent.check_isotropic()
        self.parent.check_uniform_phase()
        self.parent.mode_combox.setCurrentIndex(1)
        self.parent.selectMode(1)
        self.parent.shape_combox.setCurrentIndex(0)
    
    def ablation(self):
        self.parent.mode_combox.setCurrentIndex(0)
        self.parent.selectMode(0)
        self.parent.elements_num_spinbox.setValue(8)
        self.parent.spacing_spinbox.setValue(2)
        self.parent.beam_angle.setValue(20)
        self.parent.isotropic_checkbox.setChecked(True)
        self.parent.checkBox.setChecked(True)
        self.parent.speed_comboBox.setCurrentIndex(1)
        self.parent.freq_spinbox.setValue(2)
        self.parent.freq_comboBox.setCurrentIndex(2)  
        self.parent.check_isotropic()
        self.parent.check_uniform_phase()      
        self.parent.mode_combox.setCurrentIndex(0)  
        self.parent.shape_combox.setCurrentIndex(1)
