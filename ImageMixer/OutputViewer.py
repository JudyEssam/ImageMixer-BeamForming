from PyQt5.QtWidgets import QProgressBar, QLabel, QWidget, QRadioButton
from PyQt5.QtGui import QPixmap, QImage
import cv2
import numpy as np

class OutputViewer:
    def __init__(self, output1_widget, output2_widget, radio_button1, radio_button2, progress_bar):
        """
        Initialize the OutputViewer with widgets, radio buttons, and progress bar.

        Args:
            output1_widget (QWidget): First output widget.
            output2_widget (QWidget): Second output widget.
            radio_button1 (QRadioButton): Radio button for the first output.
            radio_button2 (QRadioButton): Radio button for the second output.
            progress_bar (QProgressBar): Progress bar widget for loading progress.
        """
        self.output1_widget = output1_widget
        self.output2_widget = output2_widget
        self.radio_button1 = radio_button1
        self.radio_button2 = radio_button2
        self.progress_bar = progress_bar

        # Create QLabel to display images on output widgets
        self.output1_label = QLabel(self.output1_widget)
        self.output1_label.setGeometry(0, 0, self.output1_widget.width(), self.output1_widget.height())
        self.output1_label.setStyleSheet("border:None")
        self.output1_label.setScaledContents(True)

        self.output2_label = QLabel(self.output2_widget)
        self.output2_label.setGeometry(0, 0, self.output2_widget.width(), self.output2_widget.height())
        self.output1_label.setStyleSheet("border:None")
        self.output2_label.setScaledContents(True)

    def whichOutput(self):
        """
        Determine which output widget should be used based on the selected radio button.

        Returns:
            QLabel: The QLabel of the selected output widget.
        """
        if self.radio_button1.isChecked():
            return self.output1_label
        elif self.radio_button2.isChecked():
            return self.output2_label
        else:
            return None  # No output selected

    def loading(self, progress):
        """
        Update the progress bar.

        Args:
            progress (int): Progress percentage (0 to 100).
        """
        self.progress_bar.setValue(progress)

    def DisplayOutput(self,inverse_image):
        """
        Display an image on the selected output widget.

        Args:
            image_path (str): Path to the image file.
        """
        output_label = self.whichOutput()
        if output_label is None:
            print("No output widget selected.")
            return

        inverse_image = np.uint8(np.clip(inverse_image, 0, 255))
        height, width = inverse_image.shape
        bytes_per_line = width
        q_image = QImage(inverse_image.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
        # Set the QPixmap to the output label
        pixmap = QPixmap.fromImage(q_image)
        output_label.setPixmap(pixmap)
        output_label.setGeometry(0, 0, output_label.parent().width(), output_label.parent().height())

        print("Image displayed successfully.")
