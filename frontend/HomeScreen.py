from PyQt5 import QtCore, QtGui, QtWidgets

from frontend.ModeSelectionScreen import UIModeSelectionScreen
from frontend.DeviceScreen import UIDeviceScreen
from frontend.PreferencesScreen import UIPreferencesScreen
from frontend.RecordsScreen import UIRecordsScreen
from frontend.StyleSheets import (QLabel_heading, QBackButton, QButtonFrame,
                                  heading_font, text_font, QWidget_background_color, QPushButton_frame,
                                  QPushButton_left1, QPushButton_right1, QPushButton_left2, QPushButton_right2)


class UIHomeScreen(QtWidgets.QWidget):
    def __init__(self, application, stacked_widget) -> None:
        super().__init__()

        self.application = application
        self.stacked_widget = stacked_widget

        self.setObjectName("HomeScreen")
        self.setStyleSheet(QWidget_background_color)
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")

        # Top Left Frame
        self.frame_top_left = QtWidgets.QFrame(self)
        self.frame_top_left.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_top_left.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_top_left.setObjectName("frame_top_left")
        self.frame_top_left.setFixedWidth(100)
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

        self.eyeTrackingLabel = QtWidgets.QLabel()
        self.eyeTrackingLabel.setFont(heading_font())
        self.eyeTrackingLabel.setStyleSheet(QLabel_heading)
        self.eyeTrackingLabel.setLineWidth(1)
        self.eyeTrackingLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.eyeTrackingLabel.setObjectName("eyeTrackingLabel")

        self.frame_top_center_layout.addWidget(self.eyeTrackingLabel)

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
        self.frame_center.setObjectName("frame_center")
        self.frame_center.setFixedHeight(400)
        self.frame_center.setStyleSheet(QPushButton_frame)

        self.logo = QtWidgets.QLabel(self.frame_center)
        self.logo.setGeometry(QtCore.QRect(80, 70, 746, 310))
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap("./media/Logo.png"))
        self.logo.setObjectName("logo")

        self.startAnalysisButton = QtWidgets.QPushButton(self.frame_center)
        self.startAnalysisButton.setGeometry(QtCore.QRect(90, 120, 211, 61))
        self.startAnalysisButton.setFont(text_font())
        self.startAnalysisButton.setStyleSheet(QPushButton_left1)
        self.startAnalysisButton.setObjectName("startAnalysisButton")
        self.startAnalysisButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.startAnalysisButton.clicked.connect(self.switch_to_mode_selection)

        self.recordsButton = QtWidgets.QPushButton(self.frame_center)
        self.recordsButton.setGeometry(QtCore.QRect(610, 120, 211, 61))
        self.recordsButton.setFont(text_font())
        self.recordsButton.setStyleSheet(QPushButton_right1)
        self.recordsButton.setObjectName("recordsButton")
        self.recordsButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.recordsButton.clicked.connect(self.switch_to_records)

        self.deviceButton = QtWidgets.QPushButton(self.frame_center)
        self.deviceButton.setGeometry(QtCore.QRect(90, 270, 211, 61))
        self.deviceButton.setFont(text_font())
        self.deviceButton.setStyleSheet(QPushButton_left2)
        self.deviceButton.setObjectName("calibrationButton")
        self.deviceButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.deviceButton.clicked.connect(self.switch_to_devices)

        self.preferencesButton = QtWidgets.QPushButton(self.frame_center)
        self.preferencesButton.setGeometry(QtCore.QRect(610, 270, 211, 61))
        self.preferencesButton.setFont(text_font())
        self.preferencesButton.setStyleSheet(QPushButton_right2)
        self.preferencesButton.setObjectName("preferences")
        self.preferencesButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.preferencesButton.clicked.connect(self.switch_to_preferences)

        self.gridLayout.addWidget(self.frame_center, 1, 0, 1, 6)

        # Bottom Left Frame
        self.frame_bottom_left = QtWidgets.QFrame(self)
        self.frame_bottom_left.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_bottom_left.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_bottom_left.setObjectName("frame_bottom_left")
        self.frame_bottom_left.setFixedWidth(100)
        self.gridLayout.addWidget(self.frame_bottom_left, 2, 0, 1, 1)

        # Bottom Center Frame
        self.frame_bottom_center = QtWidgets.QFrame(self)
        self.frame_bottom_center.setStyleSheet(QButtonFrame)
        self.frame_bottom_center.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_bottom_center.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_bottom_center.setObjectName("frame_bottom_center")
        self.gridLayout.addWidget(self.frame_bottom_center, 2, 1, 1, 4)

        # Bottom Right Frame
        self.frame_bottom_right = QtWidgets.QFrame(self)
        self.frame_bottom_right.setStyleSheet("")
        self.frame_bottom_right.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_bottom_right.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_bottom_right.setObjectName("frame_bottom_right")
        self.frame_bottom_right.setFixedWidth(100)
        self.gridLayout.addWidget(self.frame_bottom_right, 2, 5, 1, 1)

        self.retranslate_ui()

    def retranslate_ui(self) -> None:
        _translate = QtCore.QCoreApplication.translate

        self.eyeTrackingLabel.setText(_translate("HomeScreen", "EYE TRACKING"))
        self.startAnalysisButton.setText(_translate("HomeScreen", "Start Analysis"))
        self.recordsButton.setText(_translate("HomeScreen", "Records"))
        self.deviceButton.setText(_translate("HomeScreen", "Devices"))
        self.preferencesButton.setText(_translate("HomeScreen", "Preferences"))

    def switch_to_mode_selection(self) -> None:
        mode_selection_screen = UIModeSelectionScreen(self.application, self.stacked_widget)
        self.stacked_widget.addWidget(mode_selection_screen)
        self.stacked_widget.setCurrentWidget(mode_selection_screen)

    def switch_to_records(self) -> None:
        records_screen = UIRecordsScreen(self.application, self.stacked_widget, "home")
        self.stacked_widget.addWidget(records_screen)
        self.stacked_widget.setCurrentWidget(records_screen)

    def switch_to_devices(self) -> None:
        device_screen = UIDeviceScreen(self.application, self.stacked_widget)
        self.stacked_widget.addWidget(device_screen)
        self.stacked_widget.setCurrentWidget(device_screen)

    def switch_to_preferences(self) -> None:
        preferences_screen = UIPreferencesScreen(self.application, self.stacked_widget)
        self.stacked_widget.addWidget(preferences_screen)
        self.stacked_widget.setCurrentWidget(preferences_screen)
