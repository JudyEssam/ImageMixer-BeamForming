import cv2
from PyQt5.QtGui import QPixmap, QImage
from PIL import Image as IM
import numpy as np

class Image:
    def __init__(self, image_path, isGrey):
        self._image_path = image_path
        self.isGrey = isGrey
        self.image = cv2.imread(image_path) 
        

        self.convert_to_grey_scale(self.image) 
        


    def convert_to_grey_scale(self, cv_image):

        if len(cv_image.shape) == 3:  # This means it's a color image (3 channels)
            self.image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        height, width = self.image.shape
        bytes_per_line = width
        self.qimage = QImage(self.image.data, width, height, bytes_per_line, QImage.Format_Grayscale8)

    def change_brightness(self, value): 
        self.result_image = self.image.copy() 
        self.result_image = cv2.convertScaleAbs(self.result_image, alpha=1, beta=value)
        

    def change_contrast(self, value):
        self.result_image = self.image.copy() 
        self.result_image = cv2.convertScaleAbs(self.result_image, alpha=value, beta=0)

    def get_current_image(self):
        # Return the current version of the image after modifications
        return self.result_image    

        





        