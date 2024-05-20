import cv2
import ctypes
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QGraphicsOpacityEffect
from backend import Devices


def get_screen_resolution():
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
    return screen_width, screen_height


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
        self.label_center = QtWidgets.QLabel()

        top_layout = QtWidgets.QHBoxLayout()
        bottom_layout = QtWidgets.QHBoxLayout()
        # center_layout = QtWidgets.QHBoxLayout()

        top_layout.addWidget(self.label_top_left, alignment=QtCore.Qt.AlignLeft)
        top_layout.addWidget(self.label_top_right, alignment=QtCore.Qt.AlignRight)

        bottom_layout.addWidget(self.label_bottom_left, alignment=QtCore.Qt.AlignLeft)
        bottom_layout.addWidget(self.label_bottom_right, alignment=QtCore.Qt.AlignRight)

        # center_layout.addStretch(1)
        # center_layout.addWidget(self.label_center, alignment=QtCore.Qt.AlignCenter)
        # center_layout.addStretch(1)

        layout.addLayout(top_layout)
        # layout.addStretch(1)
        # layout.addLayout(center_layout)  # Add center layout
        layout.addStretch(1)
        layout.addLayout(bottom_layout)

        self.screen_width, self.screen_height = get_screen_resolution()

        self.create_aruco_markers()

        # self.set_center_marker_opacity(0.5)

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

    def set_center_marker_opacity(self, opacity):
        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(opacity)
        self.label_center.setGraphicsEffect(opacity_effect)
