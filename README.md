# PART A: Image Mixer

## Overview

This desktop application is designed to demonstrate the interplay and significance of the magnitude and phase components in the Fourier Transform (FT) of signals, using 2D images for visualization. By emphasizing the contribution of different FT components, the application allows users to explore and manipulate these elements in an intuitive way. This tool provides hands-on interaction with signal processing concepts such as FT magnitude, phase, real, and imaginary components, while enabling customized mixing and visualization.

---



## Screenshots

### Main Interface
 ![screenshot1](https://github.com/JudyEssam/ImageMixer-BeamForming/blob/9313c7b50bd04a6e04cea9bcfaf3614a614965e2/screenshots/main_interface.png
)

### Mixing Two Images
 ![screenshot2](https://github.com/JudyEssam/ImageMixer-BeamForming/blob/701d1c7ed7d220599484d2a72cee82ed63ab9c14/screenshots/mixing%20two%20images.png
)

### Region Selection and Mixer

 ![screenshot3](https://github.com/JudyEssam/ImageMixer-BeamForming/blob/40edf25108ff0b7ec9cfe82d40c4afb43629c6f1/screenshots/inner_region.png
)
 ![screenshot3](https://github.com/JudyEssam/ImageMixer-BeamForming/blob/043be5934c2651761a5085e1b762cc69b3d55b09/screenshots/outer_region.png
)
### Brightness and Contrast 
 ![screenshot4](https://github.com/JudyEssam/ImageMixer-BeamForming/blob/a07c54b4cf37db7690e39fe0a4c069f581c1edb8/screenshots/brightness_contrast.png
)

---
## Features

### **Image Viewers**
- **Open and View**: Capability to open and view four grayscale images, each displayed in a separate "viewport".
  - **Grayscale Conversion**: Automatically converts colored images to grayscale upon opening.
  - **Unified Sizes**: Ensures all opened images are displayed at the same size, adjusted to the smallest size among them.
  - **FT Components**: Each image viewport displays two components:
    1. The original image.
    2. A user-selectable Fourier Transform (FT) component, including:
       - FT Magnitude
       - FT Phase
       - FT Real
       - FT Imaginary
  - **Easy Browse**: Users can change images by double-clicking on any viewer.

### **Output Ports**
- **Two Output Viewports**: Mixer results can be displayed in one of two output viewports, identical to input image viewports.
- **User Control**: Users can determine which output viewport displays the mixer result by radiobuttons.

### **Brightness/Contrast Adjustments**
- **Interactive Changes**: Modify brightness/contrast of any displayed image or FT component using mouse dragging.
  - Drag up/down to adjust brightness.
  - Drag left/right to adjust contrast.

### **Components Mixer**
- **Customizable Weights**: Mixer output is the inverse Fourier transform (IFFT) of a weighted average of the FT of the input four images.
  - **Slider Controls**: Users can customize weights for each image FT via intuitive sliders.
  - **Support for four Components**: Adjust weights for FT Magnitude ,Phase ,Real and Imaginary.

### **Regions Mixer**
- **Region Selection**: Pick regions (inner/outer) of the FT components for mixing.
  - **Rectangle Selection**: Draw rectangles by mouse then select  a region ( inner (low frequencies) or outer (high frequencies)).
  - **Unified Regions**: Region selection applies uniformly across all four images.
  - **Customizable Size**: Adjust rectangle size by mouse.
  - **Highlighting**: Highlight selected regions with semi-transparent blue colored rectangle.

### **Realtime Mixing**
- **Progress Indication**: Lengthy IFFT operations display a progress bar to indicate the process status.
- **Cancellation Support**: Cancel ongoing operations if new settings are applied before completion.

---

# PART B: Beamforming Simulator
## Overview:
Beamforming is a fundamental concept in nowadays modern technologies starting from wireless communications, 5G,
radar, sonar to biomedical applications like ultrasound and tumor ablations. The core ideas of beamforming are delays/
phase-shifts and constructive/destructive interference.

## Video:
[](C:\mixer_beamforming\ImageMixer-BeamForming\video_beamforming\videobeamforming.mp4)


## Features:
- **Beamforming Arrays**: Create and manipulate phased arrays, including linear and circular configurations.
- **Interactive Controls**: Adjust beam angle  through slider, antenna parameters through sliders with respect to mode, and signal frequency through text field box.
- **Mode Switching**: Switch between Transmission and Receiving modes, each with its own set of controls and behavior.
- **Signal Processing**: Control signal frequency, gain, and phase for each antenna element in the array.
- **Scenario-Based Configurations**: Select different operational scenarios such as **Ultrasonic**, **5G Beamforming**, **Default**and **Tumer Ablation** through combobox.
- **Visualization**: Display **Interference Maps**, **Beam Patterns**, and other related visual outputs.
- **Slider Controls**: Fine-tune antenna phase, gain, and beam angle using sliders.
- **Speed Adjustment**: Modify the propagation speed of the signal based on selected medium (Light Speed, Ultrasound).

### Supported Modes
- **Transmission Mode**: Control parameters related to signal transmission, including interference maps and beamforming angles.
- **Receiving Mode**: Handle direction of arrival and map for receiving signals from the array.

### Array Configuration
- **Element Spacing**: Control the spacing between antennas in the array (Linear and Circular options).
- **Uniform Phase**: Adjust the phase of each antenna element.
- **Isotropic Gain**: Enable/Disable isotropic gain across antennas.

### Signal Configuration
- **Frequency Adjustment**: Modify signal frequency in various units (Hz, kHz, MHz, GHz).
- **Propagation Speed**: Choose the speed of signal propagation, considering factors like light and ultrasound speed.



### Required libraries:
  - `PyQt5`
  - `numpy`
  - `OpenCV`
  - `Pillow`
  - `Logging`
  - `matplotlib`
  - ` sys`
  - ` os`

## Acknowledgments

This project was supervised by **Dr. Tamer Basha** & **Eng. Omar**, who provided invaluable guidance and expertise throughout its development as part of the **Digital Signal Processing** course at **Cairo University Faculty of Engineering**.

![Cairo University Logo](https://imgur.com/Wk4nR0m.png)

## Contributors

- [Judy Essam](https://github.com/JudyEssam)
- [Laila Khaled](https://github.com/LailaKhaled352)
- [Fatma Elsharkawy](https://github.com/FatmaElsharkawy)
- [Hajar Ehab](https://github.com/HajarEhab)


