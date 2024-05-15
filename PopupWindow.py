import ctypes
from PyQt5 import QtCore, QtWidgets, QtGui
from frontend.StyleSheets import QControlPanelMainButton, text_font, QWidget_background_color, get_shadow, QBackButton


class PopupWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.window_width = 920
        self.window_height = 570

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setObjectName("Form")
        self.resize(self.window_width, self.window_height)
        self.setStyleSheet(QWidget_background_color)

        self.old_position = None

        self.image = QtWidgets.QLabel(self)
        self.image.setGeometry(QtCore.QRect(0, 0, self.window_width, self.window_height - 90))
        self.image.setFrameShape(QtWidgets.QFrame.Box)
        self.image.setLineWidth(0)
        self.image.setText("")
        self.image.setAlignment(QtCore.Qt.AlignCenter)
        self.image.setStyleSheet("background-color: rgb(194, 217, 255);")

        self.exitButton = QtWidgets.QPushButton(self)
        self.exitButton.setStyleSheet("QPushButton {border: none; background: transparent}")
        self.exitButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./media/Exit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.exitButton.setIcon(icon)
        self.exitButton.setIconSize(QtCore.QSize(45, 45))
        self.exitButton.setObjectName("exitButton")
        self.exitButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.exitButton.clicked.connect(self.close)
        self.exitButton.setGeometry(self.window_width - 70, 25, 45, 45)

        self.saveImage = QtWidgets.QPushButton(self)
        self.saveImage.setGeometry(QtCore.QRect(self.window_width - 210, self.window_height - 70, 200, 50))
        self.saveImage.setStyleSheet(QControlPanelMainButton)
        self.saveImage.setFont(text_font())
        self.saveImage.setObjectName("saveImage")
        self.saveImage.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.saveImage.setGraphicsEffect(get_shadow(30))

        self.color1_button = QtWidgets.QPushButton(self)
        self.color1_button.setGeometry(QtCore.QRect(self.window_width - 340, self.window_height - 70, 50, 50))
        self.color1_button.setStyleSheet("QPushButton {"
                                         "    border: 5px solid rgb(56, 65, 157);"
                                         "    background-color: black;"
                                         "    border-radius: 25px;"
                                         "}")
        self.color1_button.setText("")
        self.color1_button.setObjectName("color1")
        self.color1_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.color1_button.setGraphicsEffect(get_shadow(30))

        self.color2_button = QtWidgets.QPushButton(self)
        self.color2_button.setGeometry(QtCore.QRect(self.window_width - 270, self.window_height - 70, 50, 50))
        self.color2_button.setStyleSheet("QPushButton {"
                                         "    border: 5px solid rgb(56, 65, 157);"
                                         "    background-color: white;"
                                         "    border-radius: 25px;"
                                         "}")
        self.color2_button.setText("")
        self.color2_button.setObjectName("color2")
        self.color2_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.color2_button.setGraphicsEffect(get_shadow(30))

        self.thresholdInput = QtWidgets.QLineEdit(self)
        self.thresholdInput.setGeometry(QtCore.QRect(270, self.window_height - 70, 70, 50))
        self.thresholdInput.setStyleSheet("QLineEdit {padding: 7px; border: 3px solid rgb(56, 65, 157); "
                                          "background-color: rgb(165, 195, 255);}")
        self.thresholdInput.setFont(text_font())
        self.thresholdInput.setGraphicsEffect(get_shadow(30))
        self.thresholdInput.setAlignment(QtCore.Qt.AlignCenter)

        self.thresholdButton = QtWidgets.QPushButton(self)
        self.thresholdButton.setGeometry(QtCore.QRect(20, self.window_height - 70, 230, 50))
        self.thresholdButton.setStyleSheet(QControlPanelMainButton)
        self.thresholdButton.setFont(text_font())
        self.thresholdButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.retranslate_ui()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))
        self.saveImage.setText(_translate("Form", "Save Image"))
        self.thresholdButton.setText(_translate("Form", "Apply Threshold"))

    def mousePressEvent(self, event):
        self.old_position = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QtCore.QPoint(event.globalPos() - self.old_position)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.old_position = event.globalPos()


def setup_title_bar(outer_class):
    outer_class.getTitleBar().setFixedHeight(35)
    for button in outer_class.getTitleBar().findChildren(QtWidgets.QPushButton):
        button.setStyleSheet(
            "QPushButton {background-color: #FFE81F; border-radius: 7px; margin-right: 15px; width: 25px; height: "
            "25px} QPushButton:hover {background-color: #ccba18; border-radius: 7px; margin-right: 15px; width: "
            "25px; height: 25px} QPushButton:pressed {background-color: #ccba18; border-radius: 7px; "
            "margin-right: 15px; width: 25px; height: 25px}")
    outer_class.getTitleBar().findChildren(QtWidgets.QLabel)[1].setStyleSheet(
        "QLabel {font-size: 15px; color: #F7FAFC; font-weight: bold; margin-left: 10px}")
    outer_class.getTitleBar().findChildren(QtWidgets.QLabel)[0].setStyleSheet("QLabel {margin-left: 10px}")
