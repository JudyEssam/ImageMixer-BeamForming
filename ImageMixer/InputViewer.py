from PyQt5.QtGui import QPixmap, QPainter, QPen, QBrush,QImage
from PyQt5.QtCore import Qt, QRect, pyqtSignal
from PyQt5.QtWidgets import QLabel, QFileDialog
from Image import Image 
from ImageComponents import ImageComponents
import numpy as np
import cv2
from copy import deepcopy
from PyQt5.QtCore import QObject, pyqtSignal
from SignalEmitter import global_signal_emitter_2 
from SignalEmitter import global_signal_emitter   
class SelectableLabel(QLabel):
   
    def __init__(self,update_callback,images,image_num,mode,parent=None,shared_rect=QRect(),input_viewer=None):
        
        super().__init__(parent)
        self.setStyleSheet("border: none;")
        self.shared_rect = shared_rect
        self.update_callback = update_callback
        self.images_array = images
        
        self.image_num=image_num # This is the Image instance
        self.start_pos = None
        self.prev_y = None
        self.input_viewer=input_viewer 
        self.mode=mode
        self.original_copy= None
        self.global_signal_emitter=global_signal_emitter

    
    
    def mouseDoubleClickEvent(self, event):
        """ Handle double-click event """
        if event.button() == Qt.LeftButton:
            if self.mode == "image_widget":
                file_path, _ = QFileDialog.getOpenFileName(
                    self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.tif *.tiff)"
                )
                if file_path:
                    print(f"Double-click: Loading new image for slot {self.image_num}...")
                    self.input_viewer.displayImage(file_path, self.image_num, False, 0)
            elif self.mode == "fft_widget":
                pass
    

    def mousePressEvent(self, event):
            # self.input_viewer.useFullRegion=False 
            if event.button() == Qt.LeftButton:
                self.start_pos = event.pos()
                self.shared_rect.setTopLeft(self.start_pos)
                self.shared_rect.setBottomRight(self.start_pos)
                self.update_callback()

            elif event.button() == Qt.RightButton:
                self.is_mouse_pressed=True
                self.prev_y = event.pos().y()
                self.prev_x=event.pos().x()    
            # self.input_viewer.useFullRegion=False

    def mouseMoveEvent(self, event):
            if event.buttons() & Qt.LeftButton:
                self.shared_rect.setBottomRight(event.pos())
                self.update_callback()

            elif event.buttons() & Qt.RightButton and self.prev_y is not None and self.is_mouse_pressed:
                delta_y = event.pos().y()-self.prev_y
                # self.prev_y = event.pos().y() 
                brightness_value = delta_y
                self.images_array[self.image_num].change_brightness(brightness_value)
                updated_image = self.images_array[self.image_num].get_current_image()
                self.input_viewer.update_displayed_image(
                    self.image_num,updated_image)
                self.global_signal_emitter.function_done.emit(True)
            elif  event.buttons() & Qt.RightButton and self.prev_x is not None and self.is_mouse_pressed:   
                delta_x = event.pos().x() - self.prev_x
                contrast_value=delta_x
                self.images_array[self.image_num].change_contrast(contrast_value)
                updated_image = self.images_array[self.image_num].get_current_image()
                self.input_viewer.update_displayed_image(self.image_num,updated_image)
                self.global_signal_emitter.function_done.emit(True)

    def mouseReleaseEvent(self, event):
            if event.button() == Qt.LeftButton:
                self.shared_rect.setBottomRight(event.pos())
                self.start_pos = None
                self.update_callback()
                self.global_signal_emitter.function_done.emit(True)
                self.is_mouse_pressed=False

    def paintEvent(self, event):
                super().paintEvent(event)  # Call the base class paint event
                if self.mode == "fft_widget" and not self.shared_rect.isNull() and self.pixmap() is not None :
                    if self.shared_rect.isValid():
                        painter = QPainter(self)
                        pen = QPen(Qt.blue, 2, Qt.SolidLine)
                        painter.setPen(pen)
                        painter.setBrush(QBrush(Qt.blue, Qt.BDiagPattern))
                        painter.drawRect(self.shared_rect)



class InputViewer:
    def __init__(self):
        self.shared_rect = QRect()
        self.input1_widget = None
        self.input2_widget = None
        self.input3_widget = None
        self.input4_widget = None
        self.qimage=None
        self.isInner=True
        # self.main_window=main_window
        self.useFullRegion=True 
        self.start_pos = None
        self.rect_visible = True
        self.images = [None] * 4
        self.image_paths=[None]*4
        self.image_labels = []
        self.fft_labels=[]
        self.image_paths=[None]*4
        self.fft_components = [[None, None,None,1] for _ in range(4)]
        self.image_component=None
        self.global_signal_emitter_2=global_signal_emitter_2

    def displayImage(self, image_path, image_num, is_grey,component_index):
        if not (0 <= image_num < len(self.image_labels)):
            print(f"Invalid image number: {image_num}")
            return
        self.image_paths[image_num]=image_path        # Assuming Image is your custom class for image processing
        self.image = Image(image_path, is_grey)
        self.images[image_num]=self.image
        self.qimage_image= self.image.qimage
        pixmap_image = QPixmap.fromImage(self.qimage_image)
        
        self.fft_image=ImageComponents(self.image.image)


        if component_index == 0:
            self.fft_components[image_num][0]="magnitude"
            self.image_component = self.fft_image.get_magnitude() 
            self.fft_components[image_num][1]=self.image_component
            self.fft_components[image_num][2]= self.fft_image.get_phase()
            magintude_log= 20 * np.log(self.image_component)
            self.image_component=magintude_log

        elif component_index == 1:
            self.fft_components[image_num][0]="phase"
            self.image_component = self.fft_image.get_phase()
            self.fft_components[image_num][1]=self.fft_image.get_magnitude()
            self.fft_components[image_num][2]= self.image_component
               
        elif component_index == 2:
            self.fft_components[image_num][0]="real"
            self.image_component = self.fft_image.get_real() 
            self.fft_components[image_num][1]= self.image_component
            self.fft_components[image_num][2]= self.fft_image.get_imaginary()

            real_clipped=np.clip(self.image_component,1e-5,None)
            real_log=20 * np.log(real_clipped)
            self.image_component=real_log
            
        elif component_index == 3:
            self.fft_components[image_num][0]="imaginary"
            self.image_component = self.fft_image.get_imaginary()
            self.fft_components[image_num][1]= self.fft_image.get_real()
            self.fft_components[image_num][2]= self.image_component
            img_clipped=np.clip(self.image_component,1e-5,None)
            img_log=20 * np.log(img_clipped)
            self.image_component=img_log
        

        
        self.image_component = (self.image_component - self.image_component.min()) * (255.0 / (self.image_component.max() - self.image_component.min()))

        self.image_component = self.image_component.astype(np.uint8)

        
            


        self.qimage_fft = QImage(
        self.image_component.tobytes(),
        self.image_component.shape[1],
        self.image_component.shape[0],
        self.image_component.shape[1],
        QImage.Format_Grayscale8
    )
        pixmap_fft=QPixmap.fromImage(self.qimage_fft)
        self.fft_labels[image_num].setPixmap(pixmap_fft)
        self.fft_labels[image_num].setGeometry(
            0, 0,
            self.fft_labels[image_num].parentWidget().width(),
            self.fft_labels[image_num].parentWidget().height()
        )
        self.fft_labels[image_num].setScaledContents(True)

        self.image_labels[image_num].setPixmap(pixmap_image)
        self.image_labels[image_num].setGeometry(
            0, 0,
            self.image_labels[image_num].parentWidget().width(),
            self.image_labels[image_num].parentWidget().height()
        )
        self.image_labels[image_num].setScaledContents(True)
        print(f"Image {image_num} displayed successfully.")

        self.global_signal_emitter_2.function_done.emit(True)

    def set_image_fft_widgets(self,image_widgets,fft_widgets):
        self.image1_label = SelectableLabel(self.updateAllLabels, self.images,0,"image_widget",image_widgets[0],input_viewer=self)
        self.image2_label = SelectableLabel(self.updateAllLabels, self.images,1,"image_widget",image_widgets[1],input_viewer=self)
        self.image3_label = SelectableLabel(self.updateAllLabels, self.images,2,"image_widget",image_widgets[2],input_viewer=self)
        self.image4_label = SelectableLabel(self.updateAllLabels, self.images,3,"image_widget",image_widgets[3],input_viewer=self)


        self.fft1_label = SelectableLabel( self.updateAllLabels, self.images,0,"fft_widget",fft_widgets[0],self.shared_rect,input_viewer=self)
        self.fft2_label = SelectableLabel( self.updateAllLabels, self.images,1,"fft_widget",fft_widgets[1],self.shared_rect,input_viewer=self)
        self.fft3_label = SelectableLabel( self.updateAllLabels, self.images,2,"fft_widget",fft_widgets[2],self.shared_rect,input_viewer=self)
        self.fft4_label = SelectableLabel( self.updateAllLabels, self.images,3,"fft_widget",fft_widgets[3],self.shared_rect,input_viewer=self)

        
        self.image_labels = [self.image1_label, self.image2_label, self.image3_label, self.image4_label]
        self.fft_labels = [self.fft1_label, self.fft2_label, self.fft3_label, self.fft4_label]

        for label, widget in zip(self.image_labels, image_widgets):
            label.setGeometry(0, 0, widget.width(), widget.height())
            label.setScaledContents(True)

        for label, widget in zip(self.fft_labels, fft_widgets):
            label.setGeometry(0, 0, widget.width(), widget.height())
            label.setScaledContents(True)    

    def updateAllLabels(self):
        for label in self.fft_labels:
            label.update()

    def update_displayed_image(self, image_num, image):
        height, width = image.shape
        bytes_per_line = width
        q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(q_image)
        self.image_labels[image_num].setPixmap(pixmap)
        
    def clearRectangle(self):
        self.shared_rect = QRect()  
        for label in self.fft_labels:
            label.shared_rect = self.shared_rect
        self.updateAllLabels()
           
    def setRegion(self): 
        """
        Processes FFT components based on the shared rectangle region, ensuring valid handling of middle regions
        and applying scaling factors to adjust the selected or excluded regions.
        """
        scaled_fft_components = deepcopy(self.fft_components)
        if not scaled_fft_components:
            raise ValueError("FFT components are not set")

        for index, fft_component in enumerate(scaled_fft_components):
            if (
                self.fft_labels[index] is None
                or self.images[index] is None
                or fft_component is None
                or fft_component[2] is None
            ):
                fft_component[1] = None
                fft_component[2] = None
                continue

            if not hasattr(fft_component[2], 'shape'):
                raise ValueError(f"FFT component at index {index}[2] is invalid.")

            label = self.fft_labels[index]
            pixmap = label.pixmap()
            if pixmap is None:
                fft_component[1] = None
                fft_component[2] = None
                continue

            pixmap_width, pixmap_height = pixmap.width(), pixmap.height()
            label_width, label_height = label.width(), label.height()

            # Ensure label dimensions are non-zero
            if label_width == 0 or label_height == 0:
                raise ValueError("Label dimensions are zero, cannot calculate scaling factors.")

            scale_x = fft_component[2].shape[1] / label_width
            scale_y = fft_component[2].shape[0] / label_height

            # Calculate scaled coordinates
            x = max(0, int(self.shared_rect.x() * scale_x))
            y = max(0, int(self.shared_rect.y() * scale_y))
            width = min(fft_component[2].shape[1] - x, int(self.shared_rect.width() * scale_x))
            height = min(fft_component[2].shape[0] - y, int(self.shared_rect.height() * scale_y))

            # Handle middle region adjustments
            center_x = fft_component[2].shape[1] // 2
            center_y = fft_component[2].shape[0] // 2
            includes_center = (
                x <= center_x < x + width and y <= center_y < y + height
            )

            if self.isInner and not self.useFullRegion:
                mask = np.zeros_like(fft_component[2], dtype=np.float32)
                mask[y:y + height, x:x + width] = 1
                
               
                fft_component[1] *= mask
                fft_component[2] *= mask
                
                scaled_fft_components[index][1] = fft_component[1]
                scaled_fft_components[index][2] = fft_component[2]

            elif not self.isInner and not self.useFullRegion:
                # Create exclusion mask
                mask = np.ones_like(fft_component[2], dtype=np.float32)
                mask[y:y + height, x:x + width] = 0

                

                # Apply the mask to both components
                fft_component[1] *= mask
                fft_component[2] *= mask


                scaled_fft_components[index][1] = fft_component[1]
                scaled_fft_components[index][2] = fft_component[2]

        return scaled_fft_components






    
    def set_components(self,image1_comp,image2_comp,image3_com,image4_com):
        self.__images_comps=[image1_comp,image2_comp,image3_com,image4_com]   

    def get_components(self):
        return self.__images_comps

    def get_finalffts(self):
        return self.setRegion() 
    
    def set_components_weights(self,image_num,val):
        self.fft_components[image_num][3]= val/100.0


            
    

       

       


        
        