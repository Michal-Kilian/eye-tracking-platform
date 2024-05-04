import cv2
import ctypes
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from backend import Devices


def get_screen_resolution():
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
    return screen_width, screen_height


class ArucoOverlay(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.label_top_left = QLabel()
        self.label_top_right = QLabel()
        self.label_bottom_left = QLabel()
        self.label_bottom_right = QLabel()

        top_layout = QHBoxLayout()
        bottom_layout = QHBoxLayout()

        top_layout.addWidget(self.label_top_left, alignment=Qt.AlignLeft)
        top_layout.addWidget(self.label_top_right, alignment=Qt.AlignRight)

        bottom_layout.addWidget(self.label_bottom_left, alignment=Qt.AlignLeft)
        bottom_layout.addWidget(self.label_bottom_right, alignment=Qt.AlignRight)

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

            pixmap = QPixmap.fromImage(q_img)
            label.setPixmap(pixmap)

        for label in [self.label_top_left, self.label_top_right, self.label_bottom_left, self.label_bottom_right]:
            label.setFixedSize(corner_size + margin + margin, corner_size + margin + margin)
