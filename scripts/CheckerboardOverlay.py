import sys
from PyQt5 import QtCore, QtGui, QtWidgets


class CheckerboardOverlay(QtWidgets.QWidget):
    def __init__(self, rows=8, cols=8, square_size=50, color1=QtGui.QColor('black'), color2=QtGui.QColor('white')):
        super().__init__()
        self.rows = rows
        self.cols = cols
        self.square_size = square_size
        self.color1 = color1
        self.color2 = color2

        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint |
                            QtCore.Qt.CustomizeWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowState(QtCore.Qt.WindowFullScreen)

        screen_resolution = QtWidgets.QApplication.desktop().screenGeometry()
        self.screen_width, self.screen_height = screen_resolution.width(), screen_resolution.height()
        self.calculate_position()
        self.update_checkerboard()

    def calculate_position(self):
        self.start_x = (self.screen_width - self.cols * self.square_size) // 2
        self.start_y = (self.screen_height - self.rows * self.square_size) // 2

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        rect = self.rect()

        for row in range(self.rows):
            for col in range(self.cols):
                x = self.start_x + col * self.square_size
                y = self.start_y + row * self.square_size
                if (row + col) % 2 == 0:
                    painter.setBrush(self.color1)
                else:
                    painter.setBrush(self.color2)
                painter.drawRect(x, y, self.square_size, self.square_size)

    def resizeEvent(self, event):
        self.screen_width, self.screen_height = self.width(), self.height()
        self.calculate_position()
        self.update_checkerboard()
        self.update()

    def update_checkerboard(self):
        self.rows = min(self.rows, self.screen_height // self.square_size)
        self.cols = min(self.cols, self.screen_width // self.square_size)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()


def main():
    app = QtWidgets.QApplication(sys.argv)
    checkerboard_overlay = CheckerboardOverlay(rows=9, cols=6, square_size=120)
    checkerboard_overlay.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
