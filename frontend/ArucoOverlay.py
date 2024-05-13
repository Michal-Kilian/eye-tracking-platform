import cv2
import ctypes
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage
from backend import Devices


def get_screen_resolution():
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
    return screen_width, screen_height


class FullscreenImage(QtWidgets.QWidget):
    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path

        self.setWindowTitle('Fullscreen Image')
        self.setGeometry(0, 0, *get_screen_resolution())  # Set the window size to the screen resolution
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)  # Keep the window always on top

        self.label = QtWidgets.QLabel(self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.showFullScreen()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), QtCore.Qt.black)  # Fill the background with black
        pixmap = QtGui.QPixmap(self.image_path)
        scaled_pixmap = pixmap.scaled(self.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        painter.drawPixmap(self.rect(), scaled_pixmap)


class ArucoOverlay(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint |
                            QtCore.Qt.CustomizeWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.label_top_left = QtWidgets.QLabel()
        self.label_top_right = QtWidgets.QLabel()
        self.label_bottom_left = QtWidgets.QLabel()
        self.label_bottom_right = QtWidgets.QLabel()

        top_layout = QtWidgets.QHBoxLayout()
        bottom_layout = QtWidgets.QHBoxLayout()

        top_layout.addWidget(self.label_top_left, alignment=QtCore.Qt.AlignLeft)
        top_layout.addWidget(self.label_top_right, alignment=QtCore.Qt.AlignRight)

        bottom_layout.addWidget(self.label_bottom_left, alignment=QtCore.Qt.AlignLeft)
        bottom_layout.addWidget(self.label_bottom_right, alignment=QtCore.Qt.AlignRight)

        layout.addLayout(top_layout)
        layout.addStretch(1)
        layout.addLayout(bottom_layout)

        self.screen_width, self.screen_height = get_screen_resolution()

        self.create_aruco_markers()

    def create_aruco_markers(self):
        aruco_dict = cv2.aruco.getPredefinedDictionary(Devices.ARUCO_TYPE)
        corner_size = min(self.screen_width, self.screen_height) // 5

        margin = 20

        for i, label in enumerate(
                [self.label_top_left, self.label_top_right, self.label_bottom_left, self.label_bottom_right]):
            marker_image = cv2.aruco.generateImageMarker(aruco_dict, i, corner_size)

            marker_image = cv2.copyMakeBorder(marker_image, margin, margin, margin, margin,
                                              cv2.BORDER_CONSTANT, value=(255, 255, 255))

            marker_image_rgb = cv2.cvtColor(marker_image, cv2.COLOR_GRAY2RGB)

            q_img = QImage(marker_image_rgb.data, marker_image_rgb.shape[1], marker_image_rgb.shape[0],
                           QImage.Format_RGB888)

            pixmap = QtGui.QPixmap.fromImage(q_img)
            label.setPixmap(pixmap)

        for label in [self.label_top_left, self.label_top_right, self.label_bottom_left, self.label_bottom_right]:
            label.setFixedSize(corner_size + margin + margin, corner_size + margin + margin)

    def show_fullscreen_image(self, image_path):
        self.fullscreen_image = FullscreenImage(image_path)
        self.fullscreen_image.show()
