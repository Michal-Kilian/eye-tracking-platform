import cv2
import ctypes
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from backend import Devices


class ArucoOverlay(QWidget):
    def __init__(self):
        super().__init__()

        # Set window flags to enable transparency
        self.setWindowFlags(
            Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Set up layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # Create labels for each corner
        self.label_top_left = QLabel()
        self.label_top_right = QLabel()
        self.label_bottom_left = QLabel()
        self.label_bottom_right = QLabel()

        # Create top and bottom horizontal layouts
        top_layout = QHBoxLayout()
        bottom_layout = QHBoxLayout()

        # Add labels to top layout
        top_layout.addWidget(self.label_top_left, alignment=Qt.AlignLeft)
        top_layout.addWidget(self.label_top_right, alignment=Qt.AlignRight)

        # Add labels to bottom layout
        bottom_layout.addWidget(self.label_bottom_left, alignment=Qt.AlignLeft)
        bottom_layout.addWidget(self.label_bottom_right, alignment=Qt.AlignRight)

        # Add top and bottom layouts to main layout
        layout.addLayout(top_layout)
        layout.addStretch(1)
        layout.addLayout(bottom_layout)

        # Get screen resolution
        self.screen_width, self.screen_height = self.get_screen_resolution()

        # Create ArUco markers
        self.create_aruco_markers()

    def get_screen_resolution(self):
        user32 = ctypes.windll.user32
        screen_width = user32.GetSystemMetrics(0)
        screen_height = user32.GetSystemMetrics(1)
        return screen_width, screen_height

    def create_aruco_markers(self):
        # Define ArUco dictionary
        aruco_dict = cv2.aruco.getPredefinedDictionary(Devices.ARUCO_TYPE)

        # Calculate corner size based on screen size
        corner_size = min(self.screen_width, self.screen_height) // 10  # Adjust the size as needed

        # Generate ArUco markers for each corner
        for i, label in enumerate(
                [self.label_top_left, self.label_top_right, self.label_bottom_left, self.label_bottom_right]):
            marker_image = cv2.aruco.generateImageMarker(aruco_dict, i, corner_size)

            # Add white border
            marker_image = cv2.copyMakeBorder(marker_image, 10, 10, 10, 10,
                                              cv2.BORDER_CONSTANT, value=(255, 255, 255))

            marker_image_rgb = cv2.cvtColor(marker_image, cv2.COLOR_GRAY2RGB)

            # Convert to QImage
            q_img = QImage(marker_image_rgb.data, marker_image_rgb.shape[1], marker_image_rgb.shape[0],
                           QImage.Format_RGB888)

            # Display QImage
            pixmap = QPixmap.fromImage(q_img)
            label.setPixmap(pixmap)

        # Adjust size of labels
        for label in [self.label_top_left, self.label_top_right, self.label_bottom_left, self.label_bottom_right]:
            label.setFixedSize(corner_size + 20, corner_size + 20)
