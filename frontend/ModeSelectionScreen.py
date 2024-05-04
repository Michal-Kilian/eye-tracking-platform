from PyQt5 import QtCore, QtGui, QtWidgets
from backend import Devices, CONFIG
from frontend.AnalysisScreen import UIAnalysisScreen
from frontend.IconLabelButtonWidget import IconLabelButtonWidget
from frontend.StyleSheets import (QLabel_heading, QBackButton, QButtonFrame,
                                  heading_font, text_font, QWidget_background_color, QControlPanelMainButton,
                                  get_shadow)


class UIModeSelectionScreen(QtWidgets.QWidget):
    def __init__(self, application, stacked_widget) -> None:
        super().__init__()

        self.application = application
        self.stacked_widget = stacked_widget

        self.setObjectName("ModeSelectionScreen")
        self.setStyleSheet(QWidget_background_color)
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")

        # Top Left Frame
        self.frame_top_left = QtWidgets.QFrame(self)
        self.frame_top_left.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_top_left.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_top_left.setObjectName("frame_top_left")
        self.frame_top_left.setFixedWidth(100)

        self.frame_top_left_layout = QtWidgets.QVBoxLayout(self.frame_top_left)
        self.frame_top_left_layout.setAlignment(QtCore.Qt.AlignCenter)

        self.backButton = QtWidgets.QPushButton()
        self.backButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.backButton.setStyleSheet(QBackButton)
        self.backButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./media/BackButton.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.backButton.setIcon(icon)
        self.backButton.setIconSize(QtCore.QSize(40, 40))
        self.backButton.setObjectName("backButton")
        self.backButton.clicked.connect(self.switch_to_main)

        self.frame_top_left_layout.addWidget(self.backButton)

        self.gridLayout.addWidget(self.frame_top_left, 0, 0, 1, 1)

        # Top Left Frame 2
        self.frame_top_left_2 = QtWidgets.QFrame(self)
        self.frame_top_left_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_top_left_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_top_left_2.setObjectName("frame_top_left_2")
        self.gridLayout.addWidget(self.frame_top_left_2, 0, 1, 1, 1)

        # Top Center Frame
        self.frame_top_center = QtWidgets.QFrame(self)
        self.frame_top_center.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_top_center.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_top_center.setObjectName("frame_top_center")

        self.frame_top_center_layout = QtWidgets.QVBoxLayout(self.frame_top_center)
        self.frame_top_center_layout.setAlignment(QtCore.Qt.AlignCenter)

        self.chooseModeLabel = QtWidgets.QLabel()
        self.chooseModeLabel.setFont(heading_font())
        self.chooseModeLabel.setStyleSheet(QLabel_heading)
        self.chooseModeLabel.setLineWidth(1)
        self.chooseModeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.chooseModeLabel.setObjectName("analysisLabel")

        self.frame_top_center_layout.addWidget(self.chooseModeLabel)

        self.gridLayout.addWidget(self.frame_top_center, 0, 2, 1, 2)

        # Top Right Frame 2
        self.frame_top_right_2 = QtWidgets.QFrame(self)
        self.frame_top_right_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_top_right_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_top_right_2.setObjectName("frame_top_right_2")
        self.gridLayout.addWidget(self.frame_top_right_2, 0, 4, 1, 1)

        # Top Right Frame
        self.frame_top_right = QtWidgets.QFrame(self)
        self.frame_top_right.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_top_right.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_top_right.setObjectName("frame_top_right")
        self.frame_top_right.setFixedWidth(100)

        self.frame_top_right_layout = QtWidgets.QVBoxLayout(self.frame_top_right)
        self.frame_top_right_layout.setAlignment(QtCore.Qt.AlignCenter)

        self.exitButton = QtWidgets.QPushButton()
        self.exitButton.setStyleSheet(QBackButton)
        self.exitButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./media/Exit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.exitButton.setIcon(icon)
        self.exitButton.setIconSize(QtCore.QSize(45, 45))
        self.exitButton.setObjectName("exitButton")
        self.exitButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.exitButton.clicked.connect(application.exit)

        self.frame_top_right_layout.addWidget(self.exitButton)

        self.gridLayout.addWidget(self.frame_top_right, 0, 5, 1, 1)

        # Center Frame
        self.frame_center = QtWidgets.QFrame(self)
        self.frame_center.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_center.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_center.setObjectName("frame_center_right")
        self.frame_center.setFixedHeight(370)

        self.frame_center_layout = QtWidgets.QGridLayout(self.frame_center)

        self.real_time_widget = IconLabelButtonWidget("./media/RealTimeIcon.png", "REAL-TIME")
        self.offline_widget = IconLabelButtonWidget("./media/DataIcon.png", "OFFLINE")

        if CONFIG.MODE_SELECTED == "real-time":
            self.real_time_widget.icon_button.setStyleSheet(
                "QPushButton {text-align: center; background-color: white; border-radius: 105; border: 4px solid rgb("
                "25, 32, 80);}")
        elif CONFIG.MODE_SELECTED == "offline":
            self.offline_widget.icon_button.setStyleSheet(
                "QPushButton {text-align: center; background-color: white; border-radius: 105; border: 4px solid rgb("
                "25, 32, 80);}")

        self.real_time_widget.icon_button.clicked.connect(self.real_time_clicked)
        self.offline_widget.icon_button.clicked.connect(self.offline_clicked)

        self.frame_center_layout.addWidget(self.real_time_widget, 0, 0)
        self.frame_center_layout.addWidget(self.offline_widget, 0, 1)

        self.gridLayout.addWidget(self.frame_center, 1, 0, 1, 6)

        # Bottom Center Frame
        self.frame_bottom_center = QtWidgets.QFrame(self)
        self.frame_bottom_center.setStyleSheet(QButtonFrame)
        self.frame_bottom_center.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_bottom_center.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_bottom_center.setObjectName("frame_bottom_center")

        self.frame_bottom_center_layout = QtWidgets.QHBoxLayout(self.frame_bottom_center)

        self.continueButton = QtWidgets.QPushButton()
        self.continueButton.setFont(text_font())
        self.continueButton.setObjectName("startButton")
        self.continueButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.continueButton.setFixedSize(300, 50)
        self.continueButton.setStyleSheet(QControlPanelMainButton)
        self.continueButton.setDisabled(CONFIG.MODE_SELECTED is None)
        self.continueButton.clicked.connect(self.switch_to_analysis)
        self.continueButton.setGraphicsEffect(get_shadow(30))

        self.frame_bottom_center_layout.addWidget(self.continueButton)

        self.gridLayout.addWidget(self.frame_bottom_center, 2, 0, 1, 6)

        self.retranslate_ui()

    def retranslate_ui(self) -> None:
        _translate = QtCore.QCoreApplication.translate

        self.chooseModeLabel.setText(_translate("Form", "MODE SELECTION"))
        self.continueButton.setText(_translate("Form", "Continue"))

    def real_time_clicked(self) -> None:
        if CONFIG.MODE_SELECTED == "real-time":
            CONFIG.MODE_SELECTED = None
            self.real_time_widget.icon_button.setStyleSheet(
                "QPushButton {text-align: center; background-color: white; border-radius: 105; "
                "border: 4px solid white;}")
            self.real_time_widget.text_label.setStyleSheet("QLabel {color: rgb(56, 65, 157);}")
            self.continueButton.setDisabled(True)
        else:
            CONFIG.MODE_SELECTED = "real-time"
            self.real_time_widget.icon_button.setStyleSheet(
                "QPushButton {text-align: center; background-color: white; border-radius: 105; "
                "border: 4px solid rgb(25, 32, 80);}")
            self.offline_widget.icon_button.setStyleSheet(
                "QPushButton {text-align: center; background-color: white; border-radius: 105; "
                "border: 4px solid white;}")
            self.real_time_widget.text_label.setStyleSheet("QLabel {color: rgb(25, 32, 80);}")
            self.offline_widget.text_label.setStyleSheet("QLabel {color: rgb(56, 65, 157);}")
            self.continueButton.setDisabled(False)

    def offline_clicked(self) -> None:
        if CONFIG.MODE_SELECTED == "offline":
            CONFIG.MODE_SELECTED = None
            self.offline_widget.icon_button.setStyleSheet(
                "QPushButton {text-align: center; background-color: white; border-radius: 105; "
                "border: 4px solid white;}")
            self.offline_widget.text_label.setStyleSheet("QLabel {color: rgb(56, 65, 157);}")
            self.continueButton.setDisabled(True)
        else:
            CONFIG.MODE_SELECTED = "offline"
            self.offline_widget.icon_button.setStyleSheet(
                "QPushButton {text-align: center; background-color: white; border-radius: 105; "
                "border: 4px solid rgb(25, 32, 80);}")
            self.real_time_widget.icon_button.setStyleSheet(
                "QPushButton {text-align: center; background-color: white; border-radius: 105; "
                "border: 4px solid white;}")
            self.offline_widget.text_label.setStyleSheet("QLabel {color: rgb(25, 32, 80);}")
            self.real_time_widget.text_label.setStyleSheet("QLabel {color: rgb(56, 65, 157);}")
            self.continueButton.setDisabled(False)

    def switch_to_main(self) -> None:
        self.stacked_widget.setCurrentIndex(0)

    def switch_to_analysis(self) -> None:
        analysis_screen = UIAnalysisScreen(self.application, self.stacked_widget)
        self.stacked_widget.addWidget(analysis_screen)
        self.stacked_widget.setCurrentWidget(analysis_screen)
