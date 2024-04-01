from PyQt5 import QtWidgets, QtCore, QtGui

from frontend.StyleSheets import text_font


class Dialog(QtWidgets.QDialog):
    def __init__(self, stacked_widget):
        super().__init__()

        self.stacked_widget = stacked_widget

        self.setWindowTitle("No picture loaded")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.SplashScreen)
        self.setFixedSize(300, 250)

        self.setStyleSheet("background-color: white;")

        q_btn = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel

        self.buttonBox = QtWidgets.QDialogButtonBox(q_btn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText("Continue")
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setFont(text_font())
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setFixedWidth(133)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setStyleSheet(
            "background-color: rgb(56, 65, 157);"
            "padding: 15px 15px; margin: 3px;"
            "color: white; border-radius: 13px;")
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setText("Cancel")
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setFont(text_font())
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setFixedWidth(133)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setStyleSheet(
            "background-color: rgb(194, 217, 255);"
            "padding: 15px 15px; margin: 3px;"
            "color: rgb(25, 32, 80); border-radius: 13px;")
        self.layout = QtWidgets.QVBoxLayout()
        message = QtWidgets.QLabel("Are you sure you want to continue without a picture loaded?")
        message.setFont(text_font())
        message.setWordWrap(True)
        message.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
