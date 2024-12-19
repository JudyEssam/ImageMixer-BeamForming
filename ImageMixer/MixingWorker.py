from PyQt5.QtCore import QThread, pyqtSignal, QObject
import numpy as np
from Mixer import Mixer
from InputViewer import InputViewer

class MixingWorker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(np.ndarray)
    cancelled = pyqtSignal()

    def __init__(self, mixer, input_viewer, parent=None):
        super().__init__(parent)
        self._mixer = mixer
        self._input_viewer = input_viewer
        self._running = False

    def run(self):
        """Main execution logic for the mixing worker thread."""
        self._running = True
        try:
            # Retrieve image components and perform mixing
            image_components = self._input_viewer.get_finalffts()
            combined_result = self._mixer.set_mixing_result(image_components)
            mixed_image = self._mixer.compute_inverse_rfft(combined_result)

            # Simulate progress updates
            for i in range(0, 101, 10):
                if not self._running:
                    self.cancelled.emit()
                    return
                self.progress.emit(i)
                self.msleep(50)  # Simulate progress

            self.finished.emit(mixed_image)
        except Exception as e:
            # Handle any errors during processing
            print(f"Error in MixingWorker: {e}")
            self.cancelled.emit()

    def stop(self):
        """Stop the worker thread gracefully."""
        self._running = False
   