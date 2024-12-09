from PyQt5.QtWidgets import QMainWindow, QProgressBar ,QMessageBox, QApplication,QPushButton,QListWidget, QDoubleSpinBox ,QSpinBox, QWidget, QLabel ,  QSlider, QRadioButton, QComboBox, QTableWidget, QTableWidgetItem, QCheckBox,QMenu,QTextEdit, QDialog, QFileDialog, QInputDialog, QSizePolicy,QScrollArea,QVBoxLayout,QHBoxLayout
from PyQt5.uic import loadUi
import sys
import os
from TrasmissionMode import TransmissionMode
from RecievingMode import RecievingMode
from PhasedArray import PhasedArray
from Antenna import Antenna

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        loadUi("MainWindow.ui", self)

        self.mode_combox= self.findChild(QComboBox, 'Mode_comboBox')
        self.mode_combox.currentIndexChanged.connect(self.selectMode)
        self.mode=None
        self.phased_array=None


    def selectMode(self, index):
        if index==0:
            self.mode= TransmissionMode()
            pass
        elif index==1:
            self.mode= RecievingMode()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.showMaximized()
    sys.exit(app.exec_())        