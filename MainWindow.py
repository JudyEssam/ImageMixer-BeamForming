from PyQt5.QtWidgets import QMainWindow, QProgressBar ,QMessageBox, QApplication,QPushButton,QListWidget, QDoubleSpinBox ,QSpinBox, QWidget, QLabel ,  QSlider, QRadioButton, QComboBox, QTableWidget, QTableWidgetItem, QCheckBox,QMenu,QTextEdit, QDialog, QFileDialog, QInputDialog, QSizePolicy,QScrollArea,QVBoxLayout,QHBoxLayout
from PyQt5.uic import loadUi
import sys
import os
from Browse import Browse
from OutputViewer import OutputViewer

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        loadUi("MainWindow.ui", self)

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


        self.input_image1 = Browse(self.image1)
        self.input_image2 = Browse(self.image2)
        self.input_image3 = Browse(self.image3)
        self.input_image4 = Browse(self.image4)

        self.output_viewer = OutputViewer(self.output1, self.output2, self.RadioButton1, self.RadioButton2, self.progressbar)
        
        self.mixButton.clicked.connect(self.display_output)


    def display_output(self):
        pass
        # image_path = self.mixer.get_image_path()
        # self.output_viewer.DisplayOutput(image_path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.showMaximized()
    sys.exit(app.exec_())        