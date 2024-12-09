import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QWidget,
)
from PyQt5.QtGui import QPixmap, QPainter, QPen, QBrush
from PyQt5.QtCore import Qt, QRect


class UnifiedRectangleSelector(QLabel):
    def __init__(self, image_path, shared_rect):
        super().__init__()
        self.setPixmap(QPixmap(image_path))
        self.shared_rect = shared_rect
        self.start_pos = None
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        """Start drawing the rectangle on mouse press."""
        if event.button() == Qt.LeftButton:
            self.start_pos = event.pos()
            self.shared_rect.setTopLeft(self.start_pos)
            self.shared_rect.setBottomRight(self.start_pos)
            self.update_others()

    def mouseMoveEvent(self, event):
        """Update the rectangle as the mouse moves."""
        if self.start_pos:
            self.shared_rect.setBottomRight(event.pos())
            self.update()
            self.update_others()

    def mouseReleaseEvent(self, event):
        """Finalize the rectangle on mouse release."""
        if event.button() == Qt.LeftButton:
            self.shared_rect.setBottomRight(event.pos())
            print(f"Unified Selected Area: {self.shared_rect}")
            self.start_pos = None
            self.update()
            self.update_others()

    def paintEvent(self, event):
        """Draw the rectangle and hash the inner part in blue."""
        super().paintEvent(event)
        painter = QPainter(self)

        # Draw the rectangle
        if not self.shared_rect.isNull():
            pen = QPen(Qt.blue, 2, Qt.SolidLine)
            painter.setPen(pen)
            painter.drawRect(self.shared_rect)

            # Hash the inner region
            painter.setBrush(QBrush(Qt.blue, Qt.BDiagPattern))
            painter.drawRect(self.shared_rect)

    def update_others(self):
        """Trigger updates for all connected viewports."""
        for viewport in self.parent().parent().viewports:
            if viewport != self:
                viewport.update()


class MainWindow(QMainWindow):
    def __init__(self, image_paths):
        super().__init__()
        self.setWindowTitle("Unified Rectangle Selector with Blue Hashing")
        self.setGeometry(100, 100, 1200, 800)

        # Shared rectangle
        self.shared_rect = QRect()

        # Layout for 4 viewports
        layout = QVBoxLayout()
        top_row = QHBoxLayout()
        bottom_row = QHBoxLayout()

        self.viewports = []
        for i, image_path in enumerate(image_paths):
            viewport = UnifiedRectangleSelector(image_path, self.shared_rect)
            self.viewports.append(viewport)
            if i < 2:
                top_row.addWidget(viewport)
            else:
                bottom_row.addWidget(viewport)

        # Combine layouts
        layout.addLayout(top_row)
        layout.addLayout(bottom_row)

        # Main widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    image_paths = [
        "Images//digital_camera.jpg",  # Replace with your image paths
        "Images//dogs2.jpg",
        "Images//Michael-Moore2.jpg",
        "Images//tiger2.jpg",
    ]
    main_window = MainWindow(image_paths)
    main_window.show()
    sys.exit(app.exec_())

