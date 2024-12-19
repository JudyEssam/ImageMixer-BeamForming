class Scenarios:
    def __init__(self, parent):
        self.parent= parent
        self.parent.elements_num_spinbox.setValue(8)
        self.parent.spacing_spinbox.setValue(0.5)
        self.parent.beam_angle.setValue(20)
        self.parent.isotropic_checkbox.setChecked(True)
        self.parent.checkBox.setChecked(True)
        self.parent.Speed_spinbox.setValue(154)
        self.parent.speed_power_spinbox.setValue(1)
        self.parent.amp_spinbox.setValue(1)
        self.parent.freq_spinbox.setValue(10)
        self.parent.freq_power_spinbox.setValue(6)
        

    def ultrasonic(self):
        self.parent.elements_num_spinbox.setValue(8)
        self.parent.spacing_spinbox.setValue(0.5)
        self.parent.beam_angle.setValue(20)
        self.parent.isotropic_checkbox.setChecked(True)
        self.parent.checkBox.setChecked(True)
        self.parent.Speed_spinbox.setValue(154)
        self.parent.speed_power_spinbox.setValue(1)
        self.parent.check_isotropic()
        self.parent.check_uniform_phase()


    def beamforming_5G(self):
        self.parent.elements_num_spinbox.setValue(8)
        self.parent.spacing_spinbox.setValue(0.5)
        self.parent.beam_angle.setValue(20)
        self.parent.isotropic_checkbox.setChecked(True)
        self.parent.checkBox.setChecked(True)
        self.parent.Speed_spinbox.setValue(3)
        self.parent.speed_power_spinbox.setValue(8)
        self.parent.amp_spinbox.setValue(1)
        self.parent.freq_spinbox.setValue(2)
        self.parent.freq_power_spinbox.setValue(9)        
        self.parent.check_isotropic()
        self.parent.check_uniform_phase()
        self.parent.mode_combox.setCurrentIndex(1)
        self.parent.shape_combox.setCurrentIndex(0)
    
    def ablation(self):
        self.parent.elements_num_spinbox.setValue(8)
        self.parent.spacing_spinbox.setValue(2)
        self.parent.beam_angle.setValue(20)
        self.parent.isotropic_checkbox.setChecked(True)
        self.parent.checkBox.setChecked(True)
        self.parent.Speed_spinbox.setValue(164)
        self.parent.speed_power_spinbox.setValue(1)
        self.parent.freq_spinbox.setValue(2)
        self.parent.freq_power_spinbox.setValue(6)   
        self.parent.check_isotropic()
        self.parent.check_uniform_phase()      
        self.parent.mode_combox.setCurrentIndex(0)  
        self.parent.shape_combox.setCurrentIndex(1)
