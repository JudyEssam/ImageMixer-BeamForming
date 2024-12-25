from PyQt5.QtWidgets import QFileDialog
import cv2 
from InputViewer import InputViewer
from PyQt5.QtGui import QImage

class Browse:
    def __init__(self, widget,image_num,input_viewer):
        self._widget = widget
        self._is_grey = False
        self.image_num=image_num
        self.input_viewer=input_viewer
        self._image_path = None  # To store the selected image path
        
        self.setup_double_click_event()
        

    @property
    def image_path(self):
        return self._image_path

    @property
    def is_grey(self):
        return self._is_grey

    def setup_double_click_event(self):
        """Set up the double-click event for the widget to open the file dialog."""
        
        self._widget.mouseDoubleClickEvent = self.handle_double_click

    def handle_double_click(self, event):
        file_path, _ = QFileDialog.getOpenFileName(
            None, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.tif *.tiff)"
        )
        self.browse_image(file_path)
        if self._image_path:  # If a valid image was selected
            self.set_image()


    def browse_image(self,image_path):
        """Open file dialog to select an image.""" 
        self._image_path = image_path  
        print(self._image_path)
        self.check_extension()          
        self.check_grey_scale()

        self.set_image()    


    def set_image(self):
        if not self._image_path:
            print("Image path is not set.")
            return 
        self.input_viewer.displayImage(self._image_path, self.image_num,self._is_grey,0) 


            
              

    def check_extension(self):
        """Check if the file has a valid image extension."""
        valid_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff']
        if not any(self._image_path.lower().endswith(ext) for ext in valid_extensions):
            print("Invalid image file extension.")
            self._image_path = None  # Clear the image path if invalid
            return False
        print("Valid image file extension.")
        return True

    def check_grey_scale(self):
        """Check if the image is grayscale."""
        image = cv2.imread(self._image_path)
        if image is None:
            print("Failed to load the image.")
            return False
        
        if len(image.shape) < 3:  # Single channel means grayscale
            self._is_grey = True
        else:
            b, g, r = cv2.split(image)
            self._is_grey = cv2.countNonZero(b - g) == 0 and cv2.countNonZero(b - r) == 0
        
        if self.is_grey:
            print("The selected image is grayscale.")
        else:
            print("The selected image is not grayscale.")
        
        return self.is_grey