from PyQt5 import QtWidgets, QtCore
import ctypes


def get_screen_resolution():
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
    return screen_width, screen_height


class GazePointOverlay(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint |
                            QtCore.Qt.CustomizeWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.5)
        self.screen_width, self.screen_height = get_screen_resolution()
        self.setGeometry(0, 0, self.screen_width, self.screen_height)

        self.gaze_label = QtWidgets.QLabel(self)
        self.gaze_label.setStyleSheet("QLabel {background-color: red; border-radius: 15px}")
        self.gaze_label.resize(30, 30)

        self.gaze_x, self.gaze_y = None, None

    def update_gaze_point(self, uv_x, uv_y):

        gaze_x = uv_x * self.screen_width
        gaze_y = uv_y * self.screen_height

        self.gaze_label.move(gaze_x, gaze_y)
