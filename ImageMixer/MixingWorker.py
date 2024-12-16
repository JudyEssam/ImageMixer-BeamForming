from PyQt5.QtCore import QThread, pyqtSignal, QObject
import numpy as np
from Mixer import Mixer
from InputViewer import InputViewer

class MixingWorker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(np.ndarray)
    cancelled = pyqtSignal()

    def __init__(self, mixer, input_viewer):
        super().__init__()
        self.mixer = mixer
        self.input_viewer = input_viewer
        self._is_running = True

    def run(self):
            self._is_running = True
        
            imge_components = self.input_viewer.get_finalffts()
            combined_result = self.mixer.set_mixing_result(imge_components)
            self.mixed_image = self.mixer.compute_inverse_rfft(combined_result)

            # Update progress
            for i in range(0, 101, 10):
                if not self._is_running:
                    self.cancelled.emit()
                    return
                self.progress.emit(i)
                self.msleep(50)  # Simulate progress

            self.finished.emit(self.mixed_image)
       

    def stop(self):
        self._is_running = False
