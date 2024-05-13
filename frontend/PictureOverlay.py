import ctypes
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage
from backend import Devices


def get_screen_resolution():
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
    return screen_width, screen_height


class PictureOverlay(QtWidgets.QWidget):
    def __init__(self, image_path):
        super().__init__()

        self.setWindowTitle('Picture Overlay')
        self.setGeometry(100, 100, 800, 600)  # Initial window size
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)  # Keep the window always on top

        layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(layout)

        # Create a QLabel widget to display the image
        self.image_label = QtWidgets.QLabel(self)
        layout.addWidget(self.image_label)

        # Load the image and set it to the QLabel
        pixmap = QtGui.QPixmap(image_path)
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)

        # Maximize the window to fullscreen
        self.showFullScreen()
