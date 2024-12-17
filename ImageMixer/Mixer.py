import numpy as np
import cv2
from ImageComponents import ImageComponents
import logging



class Mixer:

    def __init__(self):
        self.combined_complex_result = None   # Store combined complex result
        logging.info("Mixer class initialized.")

    def set_mixing_result(self, image_components):
        try:
            if len(image_components) != 4:
                raise ValueError("Input must contain 4 lists for 4 images.")
            logging.info("Processing mixing result with 4 image components.")

            # Filter out None components
            non_none_components = [component for component in image_components if component is not None]
            if not non_none_components:
                raise ValueError("All image components are None.")
            
            # Find the largest width and height among all non-None images
            max_height = max([component[1].shape[0] for component in non_none_components if component[1] is not None])
            max_width = max([component[1].shape[1] for component in non_none_components if component[1] is not None])
            logging.debug(f"Maximum dimensions calculated: max_height={max_height}, max_width={max_width}")

            # Resize and pad all images to the largest size (max_height, max_width)
            padded_components = []
            for i, component in enumerate(image_components):
                if component is None:
                    logging.warning(f"Image component {i} is None, initializing with zeros.")
                    mode = "real"  # Default to 'real' mode if None
                    list1 = np.zeros((max_height, max_width))
                    list2 = np.zeros((max_height, max_width))
                    gain = 0
                else:
                    mode, list1, list2, gain = component

                    if mode is None:
                        logging.error(f"Invalid mode 'None' at index {i}. Defaulting to 'real'.")
                        mode = "real"  # Set a default mode if None

                    if mode not in ["real", "imaginary", "magnitude", "phase"]:
                        raise ValueError(f"Invalid mode '{mode}' at index {i}. Must be 'real', 'imaginary', 'magnitude', or 'phase'.")

                    if list1 is None or list2 is None:
                        logging.warning(f"One of the lists for component {i} is None, initializing with zeros.")
                        list1 = np.zeros((max_height, max_width))
                        list2 = np.zeros((max_height, max_width))

                # Get the current image shape
                current_height, current_width = list1.shape

                # Calculate padding amounts for each side (top, bottom, left, right)
                pad_height_top = (max_height - current_height) // 2
                pad_height_bottom = max_height - current_height - pad_height_top
                pad_width_left = (max_width - current_width) // 2
                pad_width_right = max_width - current_width - pad_width_left

                # Apply padding using numpy.pad
                list1_padded = np.pad(list1, ((pad_height_top, pad_height_bottom), (pad_width_left, pad_width_right)), mode='constant')
                list2_padded = np.pad(list2, ((pad_height_top, pad_height_bottom), (pad_width_left, pad_width_right)), mode='constant')

                padded_components.append([mode, list1_padded, list2_padded, gain])
                logging.debug(f"Image {i} padded to {list1_padded.shape}.")

            # Initialize arrays to hold all the real and imaginary parts
            real_array = np.zeros((max_height, max_width))
            imaginary_array = np.zeros((max_height, max_width))

            # Loop through the components and update the arrays
            for i, component in enumerate(padded_components):
                mode, list1, list2, gain = component
                logging.info(f"Processing image {i} - Mode: {mode}, Gain: {gain}")

                # Apply gain to the appropriate list based on the mode
                if mode == "real":
                    real_array += list1 * gain  # Add to real part
                elif mode == "imaginary":
                    imaginary_array += list2 * gain  # Add to imaginary part
                elif mode == "magnitude":
                    real_array += list1 * gain  # Add to real part (magnitude mode directly modifies real array)
                elif mode == "phase":
                    imaginary_array += list2 * gain  # Add to imaginary part (phase mode directly modifies imaginary array)
                else:
                    logging.error(f"Invalid mode '{mode}' at index {i}.")
                    raise ValueError(f"Invalid mode '{mode}' at index {i}. Must be 'real', 'imaginary', 'magnitude', or 'phase'.")

            # Convert to complex form based on the mode
            if "magnitude" in [component[0] for component in padded_components] or "phase" in [component[0] for component in padded_components]:
                complex_result = real_array * np.exp(1j * imaginary_array)
            else:
                # If only real and imaginary parts are used, combine them directly
                complex_result = real_array + 1j * imaginary_array

            # Print the shapes of the final real and imaginary arrays
            print(f"Real array shape: {real_array.shape}")
            print(f"Imaginary array shape: {imaginary_array.shape}")

            # Store the combined complex result
            self.combined_complex_result = complex_result
            logging.info("Mixing result successfully computed.")

            # Reset real_array and imaginary_array to zeros after computation
            real_array.fill(0)
            imaginary_array.fill(0)

            # Log that the arrays have been reset
            logging.info("Real and Imaginary arrays have been reset.")

            return self.combined_complex_result

        except Exception as e:
            logging.error(f"Error in set_mixing_result: {e}")
            raise

    def compute_inverse_rfft(self, combined_result):
        try:
            if combined_result is None:
                raise ValueError("Combined complex result has not been computed. Call set_mixing_result first.")

            if not isinstance(combined_result, np.ndarray):
                combined_result = np.array(combined_result, dtype=np.complex128)

            logging.info("Performing inverse RFFT.")
            inverse_result = ImageComponents.compute_inverse_rfft(combined_result)
            
            logging.info("Inverse RFFT computation completed.")
            return inverse_result
        except Exception as e:
            logging.error(f"Error in compute_inverse_rfft: {e}")
            raise
