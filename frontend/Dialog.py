from PyQt5 import QtWidgets, QtCore
from frontend.StyleSheets import Fonts, GlobalStyleSheet, DialogStyleSheet


class Dialog(QtWidgets.QDialog):
    def __init__(self, stacked_widget: QtWidgets.QStackedWidget, window_title: str, submit_text: str,
                 cancel_text: str, message: str) -> None:
        super().__init__()

        self.stacked_widget = stacked_widget

        self.setWindowTitle(window_title)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.SplashScreen)
        self.setFixedSize(300, 250)

        self.setStyleSheet(GlobalStyleSheet.WhiteBackgroundColor)

        q_btn = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel

        self.buttonBox = QtWidgets.QDialogButtonBox(q_btn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText(submit_text)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setFont(Fonts.TextFont())
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setFixedWidth(133)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setStyleSheet(DialogStyleSheet.ButtonOK)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setText(cancel_text)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setFont(Fonts.TextFont())
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setFixedWidth(133)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setStyleSheet(DialogStyleSheet.ButtonCancel)
        self.layout = QtWidgets.QVBoxLayout()
        message = QtWidgets.QLabel(message)
        message.setFont(Fonts.TextFont())
        message.setWordWrap(True)
        message.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
