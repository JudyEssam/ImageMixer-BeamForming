import numpy as np
import matplotlib.pyplot as plt

class LinearArrayBeamforming:
    def __init__(self, num_elements, antenna_spacing, frequency, steering_angle):
        self.num_elements = num_elements  # Number of antenna elements
        self.antenna_spacing = antenna_spacing  # Spacing between elements (in meters)
        self.frequency = frequency  # Operating frequency (in Hz)
        self.steering_angle = steering_angle  # Steering angle (in degrees)

        self.wavelength = 3e8 / self.frequency  # Wavelength (in meters)
        self.k = 2 * np.pi / self.wavelength  # Wavenumber

        # Calculate the steering vector
        self.steer_vector = self.calculate_steering_vector()

    def calculate_steering_vector(self):
        # Steering vector formula for a linear array
        n = np.arange(self.num_elements)  # Element index
        theta = np.radians(self.steering_angle)  # Convert steering angle to radians

        # Calculate the phase shifts for each element
        phase_shifts = np.exp(1j * self.k * self.antenna_spacing * n * np.sin(theta))

        return phase_shifts

    def calculate_beam_pattern(self):
        # Compute the beam pattern using the steering vector
        N_fft = 512  # Number of FFT points for better resolution
        steer_vector_padded = np.concatenate([self.steer_vector, np.zeros(N_fft - self.num_elements)])
        steer_vector_fft = np.fft.fftshift(np.fft.fft(steer_vector_padded))  # Compute the FFT
        steer_vector_fft_dB = 10 * np.log10(np.abs(steer_vector_fft)**2)  # Convert to dB

        return steer_vector_fft_dB

    def plot_beam_pattern(self):
        # Plot the beam pattern in polar coordinates
        steer_vector_fft_dB = self.calculate_beam_pattern()

        # Map FFT bins to angles in radians
        N_fft = 512
        theta_bins = np.arcsin(np.linspace(-1, 1, N_fft))  # Bin positions in radians

        # Plot the beam pattern
        plt.figure(figsize=(6, 6))
        plt.subplot(111, projection='polar')
        plt.plot(theta_bins, steer_vector_fft_dB)  # Plot beam pattern in dB

        # Mark the peak
        theta_max = theta_bins[np.argmax(steer_vector_fft_dB)]
        plt.plot([theta_max], [np.max(steer_vector_fft_dB)], 'ro')  # Peak position
        plt.text(theta_max, np.max(steer_vector_fft_dB) - 5,
                 f"{np.round(theta_max * 180 / np.pi)}°", color='white')  # Annotate peak in degrees

        plt.title("Beam Pattern for Linear Array", color="white")
        plt.ylim([-50, 0])  # Set the y-axis limits for the dB scale
        plt.show()

# Example usage
num_elements = 10  # Number of antennas in the array
antenna_spacing = 0.5  # Antenna spacing in meters
frequency = 2.4e9  # Frequency in Hz (e.g., 2.4 GHz)
steering_angle = 20  # Steering angle in degrees

beamforming = LinearArrayBeamforming(num_elements, antenna_spacing, frequency, steering_angle)
beamforming.plot_beam_pattern()
