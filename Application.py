from PyQt5 import QtCore, QtWidgets
from frontend.HomeScreen import UIHomeScreen
from frontend.StyleSheets import GlobalStyleSheet
from backend import CONFIG


class UIMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.old_position = None

    def mousePressEvent(self, event):
        self.old_position = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QtCore.QPoint(event.globalPos() - self.old_position)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.old_position = event.globalPos()


def main() -> None:
    import sys

    app = QtWidgets.QApplication(sys.argv)

    if len(sys.argv) > 1 and sys.argv[1] in ['--test', '-T']:
        CONFIG.TEST = True

    window = UIMainWindow()

    stacked_widget = QtWidgets.QStackedWidget()
    stacked_widget.setStyleSheet(GlobalStyleSheet.StackedWidget)

    home_screen = UIHomeScreen(app, stacked_widget)
    stacked_widget.addWidget(home_screen)

    window.setCentralWidget(stacked_widget)
    window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    window.setFixedSize(920, 570)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
