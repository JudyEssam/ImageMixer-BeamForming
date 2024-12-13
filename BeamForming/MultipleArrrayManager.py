import numpy as np

class ArrayManager:
    def __init__(self):
        self._arrays = []

    def add_array(self, array):
        self._arrays.append(array)

    def calculate_combined_field(self, observation_points, signal_wavelength):
        combined_field = np.zeros(len(observation_points), dtype=complex)

        for array in self._arrays:
            array_position = array.get_position()

            for idx, (x_obs, y_obs) in enumerate(observation_points):
                distance = np.sqrt((x_obs - array_position[0])**2 + (y_obs - array_position[1])**2)
                phase_shift = -2j * np.pi * distance / signal_wavelength
                combined_field[idx] += np.sum(array._steer_vector * np.exp(phase_shift))

        return combined_field
