from PyQt5.QtWidgets import QMainWindow, QProgressBar ,QMessageBox, QApplication,QPushButton,QListWidget, QDoubleSpinBox ,QSpinBox, QWidget, QLabel ,  QSlider, QRadioButton, QComboBox, QTableWidget, QTableWidgetItem, QCheckBox,QMenu,QTextEdit, QDialog, QFileDialog, QInputDialog, QSizePolicy,QScrollArea,QVBoxLayout,QHBoxLayout
from PyQt5.uic import loadUi
import sys
import os
from Browse import Browse
from OutputViewer import OutputViewer
from InputViewer import InputViewer 
import logging
from Mixer import Mixer
from MixingWorker import MixingWorker
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        loadUi("MainWindow.ui", self)

        logging.basicConfig(
            filename='app.log',           # Log file name
            level=logging.DEBUG,          # Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            format='%(asctime)s - %(levelname)s - %(message)s'  # Log message format
                )
        
        
        self.mixer=Mixer()
        self.progressbar= self.findChild(QProgressBar, "progressBar_3" )
        self.output1 = self.findChild(QWidget, "output_1")
        self.output2 = self.findChild(QWidget, "output_2")
        self.mixButton = self.findChild(QPushButton, "mixxer_3")        
        self.RadioButton1 = self.findChild(QRadioButton, "radioButton1")
        self.RadioButton2 = self.findChild(QRadioButton, "radioButton2")
        self.image1 = self.findChild(QWidget, "original_1")
        self.image2 = self.findChild(QWidget, "original_2")
        self.image3 = self.findChild(QWidget, "original_3")
        self.image4 = self.findChild(QWidget, "original_4")
        self.RadioButton1.setChecked(True)

        self.images_widgets=[self.image1,self.image2,self.image3,self.image4]
        
        self.fft_widget2 = self.findChild(QWidget, "component_image_2")
        self.fft_widget1 = self.findChild(QWidget, "component_image_1")
        self.fft_widget3 = self.findChild(QWidget, "component_image_3")
        self.fft_widget4 = self.findChild(QWidget, "component_image_4")

        self.fft_widgets=[self.fft_widget1,self.fft_widget2,self.fft_widget3,self.fft_widget4]

        self.image1_combobox=self.findChild(QComboBox, "combo1_6")
        self.image2_combobox=self.findChild(QComboBox, "combo1_7")
        self.image3_combobox=self.findChild(QComboBox, "combo1_8")
        self.image4_combobox=self.findChild(QComboBox, "combo1_9")


        self.isInner_radiobutton=self.findChild(QRadioButton,"radioButton_In_3")
        self.isOuter_radiobutton=self.findChild(QRadioButton,"radioButton_Out_3")
        self.deselect_region= self.findChild(QPushButton,"Deselect_3")

        self.image1_slider=self.findChild(QSlider,"Slider_weight3_5")
        self.image2_slider=self.findChild(QSlider,"Slider_weight3_6")
        self.image3_slider=self.findChild(QSlider,"Slider_weight3_7")
        self.image4_slider=self.findChild(QSlider,"Slider_weight3_8")

        self.image1_slider.setRange(0,100)
        self.image1_slider.setSingleStep(10)

        self.image2_slider.setRange(0,100)
        self.image2_slider.setSingleStep(10)

        self.image3_slider.setRange(0,100)
        self.image3_slider.setSingleStep(10)

        self.image4_slider.setRange(0,100)
        self.image4_slider.setSingleStep(10)

        self.input_viewer = InputViewer()
        self.input_viewer.set_image_fft_widgets(self.images_widgets,self.fft_widgets) 
        self.deselect_region.clicked.connect(self.input_viewer.clearRectangle) 
        # self.input_viewer.selectRegion(self.input_viewer.images,self.input_viewer.labels)
        self.isInner_radiobutton.clicked.connect(self.inner_region_state)
        self.isOuter_radiobutton.clicked.connect(self.outer_region_state)
        self.deselect_region.clicked.connect(self.full_region_state)

        self.image1_slider.valueChanged.connect(lambda: self.update_componant1_weight(0))
        self.image2_slider.valueChanged.connect(lambda: self.update_componant2_weight(1))
        self.image3_slider.valueChanged.connect(lambda: self.update_componant3_weight(2))
        self.image4_slider.valueChanged.connect(lambda: self.update_componant4_weight(3))

        self.input_image1 = Browse(self.image1,0,self.input_viewer)
        self.input_image2 = Browse(self.image2,1,self.input_viewer)
        self.input_image3 = Browse(self.image3,2,self.input_viewer)
        self.input_image4 = Browse(self.image4,3,self.input_viewer)
        self.input_image1.set_image()
        self.input_image2.set_image()
        self.input_image3.set_image()
        self.input_image4.set_image()

        self.image1_combobox.currentIndexChanged.connect(
            lambda index: self.input_viewer.displayImage(self.input_image1._image_path, 0, self.input_image1._is_grey, index)
        )
        self.image2_combobox.currentIndexChanged.connect(
            lambda index: self.input_viewer.displayImage(self.input_image2._image_path, 1, self.input_image2._is_grey, index)
        )
        self.image3_combobox.currentIndexChanged.connect(
            lambda index: self.input_viewer.displayImage(self.input_image3._image_path, 2, self.input_image3._is_grey, index)
        )
        self.image4_combobox.currentIndexChanged.connect(
            lambda index: self.input_viewer.displayImage(self.input_image4._image_path, 3, self.input_image4._is_grey, index)
        )


        self.output_viewer = OutputViewer(self.output1, self.output2, self.RadioButton1, self.RadioButton2, self.progressbar)
                
        

        self.worker = None
        self.mixButton.clicked.connect(self.start_mixing)
    def closeEvent(self, event):
        if self.worker is not None:
            self.worker.stop()
            self.worker.wait()
        event.accept()
    def update_componant1_weight(self,image_num):
        self.input_viewer.set_components_weights(image_num,self.image1_slider.value())
        print(self.input_viewer.fft_components[image_num][1].shape)

    def update_componant2_weight(self,image_num):
        self.input_viewer.set_components_weights(image_num,self.image2_slider.value())

    def update_componant3_weight(self,image_num):
        self.input_viewer.set_components_weights(image_num,self.image3_slider.value())

    def update_componant4_weight(self,image_num):
        self.input_viewer.set_components_weights(image_num,self.image4_slider.value())
            


    def inner_region_state(self):
        self.input_viewer.isInner=True
        self.input_viewer.useFullRegion=False
    def outer_region_state(self):
        self.input_viewer.isInner=False
        self.input_viewer.useFullRegion=False
    def full_region_state(self):
        self.input_viewer.useFullRegion=True        

    def start_mixing(self):
        if self.worker is not None:
            self.worker.stop()
            self.worker.wait()

        self.worker = MixingWorker(self.mixer, self.input_viewer)
        self.worker.progress.connect(self.output_viewer.loading)
        self.worker.finished.connect(self.display_output)
        self.worker.start()

    def display_output(self,mixed_image):
        self.output_viewer.DisplayOutput(mixed_image)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.showMaximized()
    sys.exit(app.exec_())        