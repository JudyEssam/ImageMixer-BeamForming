import numpy as np
import cv2
from numpy.fft import fft2,rfft2, irfft2, fftshift, ifftshift

class ImageComponents:
    def __init__(self, image):
        """
        Initialize the ImageRFFT class with a real-valued image.
        :param image: Input image as a NumPy array.
        """
        if not isinstance(image, np.ndarray):
            raise ValueError("Input must be a NumPy array representing the image.")
        
        self.__original_image = image
        self.__rfft_result = None
        self.__magnitude = None
        self.__phase = None
        self.__real = None
        self.__imaginary = None
        self.__inverse_image = None

        self.__compute_rfft()

    def __compute_rfft(self):
       
        self.__rfft_result = fft2(self.__original_image)
        self.__rfft_result = fftshift(self.__rfft_result)  # Center the FFT
        
      
        self.__magnitude = np.abs(self.__rfft_result)
        self.__phase = np.angle(self.__rfft_result)
        self.__real = np.real(self.__rfft_result)
        self.__imaginary = np.imag(self.__rfft_result)

    def compute_inverse_rfft(self,mix_result):
        
        if mix_result is None:
            raise ValueError("RFFT has not been computed.")
        
        # Shift back and perform inverse RFFT
        ifft_shifted = ifftshift(mix_result)
        self.__inverse_image = np.real(irfft2(ifft_shifted))
        return self.__inverse_image

    # Setter methods to update the components with copies
    def set_magnitude(self, magnitude):
        self.__magnitude = np.copy(magnitude)

    def set_phase(self, phase):
        self.__phase = np.copy(phase)

    def set_real(self, real):
        self.__real = np.copy(real)

    def set_imaginary(self, imaginary):
        self.__imaginary = np.copy(imaginary)

    # Getter methods
    def get_magnitude(self):
        return np.copy(self.__magnitude)

    def get_phase(self):
        return np.copy(self.__phase)

    def get_real(self):
        return np.copy(self.__real)

    def get_imaginary(self):
        return np.copy(self.__imaginary)

    def get_original_image(self):
        return np.copy(self.__original_image)

    def get_inverse_image(self):
        if self.__inverse_image is None:
            raise ValueError("Inverse RFFT has not been computed yet. Call compute_inverse_rfft() first.")
        return np.copy(self.__inverse_image)
