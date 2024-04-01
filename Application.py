from PyQt5 import QtCore, QtWidgets

from frontend.HomeScreen import UIHomeScreen
from frontend.StyleSheets import QStackedWidget


def main() -> None:
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()

    stacked_widget = QtWidgets.QStackedWidget()
    stacked_widget.setStyleSheet(QStackedWidget)

    home_screen = UIHomeScreen(app, stacked_widget)
    stacked_widget.addWidget(home_screen)

    window.setCentralWidget(stacked_widget)
    window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    window.setFixedSize(920, 570)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
