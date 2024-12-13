import numpy as np
from ImageComponents import ImageComponents

class Mixer:

    def __init__(self):
        self.combined_complex_result = []   # To store the combined complex result of all images

    def set_mixing_result(self, image_components):
        """
        Process the image components and apply gain values to compute the complex form.

        Parameters:
        image_components (list): A list of 4 lists, where each inner list represents an image with the following structure:
                                 [string ('real', 'imaginary', 'magnitude', 'phase'),
                                  list (real/magnitude components),
                                  list (imaginary/phase components),
                                  float (gain value)]
        """
        if len(image_components) != 4:
            raise ValueError("Input must contain 4 lists for 4 images.")

        combined_complex_result = None  # Initialize combined result

        for i, component in enumerate(image_components):
            if len(component) != 4:
                raise ValueError(f"Each image component must have 4 elements. Error at index {i}.")

            mode, list1, list2, gain = component

            # Convert lists to numpy arrays for efficient processing
            list1 = np.array(list1)
            list2 = np.array(list2)

            # Apply gain to the appropriate list based on the mode
            if mode == "real":
                real = list1 * gain
                imaginary = list2
                complex_result = real + 1j * imaginary

            elif mode == "imaginary":
                real = list1
                imaginary = list2 * gain
                complex_result = real + 1j * imaginary

            elif mode == "magnitude":
                magnitude = list1 * gain
                phase = list2
                complex_result = magnitude * np.exp(1j * phase)

            elif mode == "phase":
                magnitude = list1
                phase = list2 * gain
                complex_result = magnitude * np.exp(1j * phase)

            else:
                raise ValueError(f"Invalid mode '{mode}' at index {i}. Must be 'real', 'imaginary', 'magnitude', or 'phase'.")

            self.combined_complex_result.extend(complex_result)

        return self.combined_complex_result

    def compute_inverse_rfft(self,combined_result):
        """
        Perform the inverse RFFT for the combined complex result and update the ImageComponents object.
        """
        combined_result=combined_result
        if combined_result is None:
            raise ValueError("Combined complex result has not been computed. Call set_mixing_result first.")

        image_components_obj = ImageComponents(np.zeros_like(combined_result))  # Dummy image array for initialization
        image_components_obj.compute_inverse_rfft(combined_result)
       
    



    