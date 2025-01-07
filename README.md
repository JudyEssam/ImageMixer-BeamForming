# Fourier Transform Mixer

## Overview

This desktop application is designed to demonstrate the interplay and significance of the magnitude and phase components in the Fourier Transform (FT) of signals, using 2D images for visualization. By emphasizing the contribution of different FT components, the application allows users to explore and manipulate these elements in an intuitive way. This tool provides hands-on interaction with signal processing concepts such as FT magnitude, phase, real, and imaginary components, while enabling customized mixing and visualization.

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

## Screenshots

### Main Interface
 ![screenshot1](https://github.com/JudyEssam/ImageMixer-BeamForming/blob/9313c7b50bd04a6e04cea9bcfaf3614a614965e2/screenshots/main_interface.png
)

### Mixing Two Images
 ![screenshot2](
)

### Region Selection and Mixer

 ![screenshot3](https://github.com/JudyEssam/ImageMixer-BeamForming/blob/40edf25108ff0b7ec9cfe82d40c4afb43629c6f1/screenshots/inner_region.png
)
 ![screenshot3](
)

### Brightness and Contrast 
 ![screenshot4](https://github.com/JudyEssam/ImageMixer-BeamForming/blob/a07c54b4cf37db7690e39fe0a4c069f581c1edb8/screenshots/brightness_contrast.png
)

---
### Required libraries:
  - `PyQt5`
  - `numpy`
  - `OpenCV`
  - `Pillow`
  - `Logging`


