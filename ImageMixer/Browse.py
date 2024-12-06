from PyQt5.QtWidgets import QFileDialog
import cv2

class Browse:
    def __init__(self, widget):
        self._widget = widget
        self._is_grey = False
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
        """Handle the double-click event to open the file dialog and process the image."""
        self.browse_image()

    def browse_image(self):
        """Open file dialog to select an image."""
        file_path, _ = QFileDialog.getOpenFileName(
            None, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.tif *.tiff)"
        )
        if file_path:
            self._image_path = file_path  # Set the image path directly
            self.check_extension()          # Check the extension
            self.check_grey_scale()        # Check if the image is grayscale

    def check_extension(self):
        """Check if the file has a valid image extension."""
        valid_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff']
        if not any(self.image_path.lower().endswith(ext) for ext in valid_extensions):
            print("Invalid image file extension.")
            self._image_path = None  # Clear the image path if invalid
            return False
        print("Valid image file extension.")
        return True

    def check_grey_scale(self):
        """Check if the image is grayscale."""
        image = cv2.imread(self.image_path)
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