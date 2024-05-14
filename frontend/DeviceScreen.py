import uvc
from PyQt5 import QtCore, QtGui, QtWidgets
from frontend.StyleSheets import (QLabel_heading, QBackButton, QButtonFrame,
                                  heading_font, QWidget_background_color, text_font, QLabel_device,
                                  QComboBox_device, QControlPanelMainButton, QControlPanelButton, qcombobox_font,
                                  QDevicePreviewButton, QRefreshButton, QComboBox_selected, get_shadow)
from backend import Devices
from DevicePreview import DevicePreview


class UIDeviceScreen(QtWidgets.QWidget):
    def __init__(self, application, stacked_widget) -> None:
        super().__init__()

        self.stacked_widget = stacked_widget
        self.device_preview = None

        self.setObjectName("DeviceScreen")
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

        self.calibrationLabel = QtWidgets.QLabel()
        self.calibrationLabel.setFont(heading_font())
        self.calibrationLabel.setStyleSheet(QLabel_heading)
        self.calibrationLabel.setLineWidth(1)
        self.calibrationLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.calibrationLabel.setObjectName("calibrationLabel")

        self.frame_top_center_layout.addWidget(self.calibrationLabel)

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
        self.frame_center.setFixedHeight(370)

        self.frame_center_layout = QtWidgets.QGridLayout(self.frame_center)
        self.frame_center_layout.setAlignment(QtCore.Qt.AlignCenter)

        self.right_eye_select = QtWidgets.QComboBox()
        self.right_eye_select.setStyleSheet(QComboBox_device)
        self.right_eye_select.setFixedWidth(350)
        self.right_eye_select.setFont(qcombobox_font())
        self.right_eye_select.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.right_eye_select.setGraphicsEffect(get_shadow(30))

        self.left_eye_select = QtWidgets.QComboBox()
        self.left_eye_select.setStyleSheet(QComboBox_device)
        self.left_eye_select.setFixedWidth(350)
        self.left_eye_select.setFont(qcombobox_font())
        self.left_eye_select.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.left_eye_select.setGraphicsEffect(get_shadow(30))

        self.world_select = QtWidgets.QComboBox()
        self.world_select.setStyleSheet(QComboBox_device)
        self.world_select.setFixedWidth(350)
        self.world_select.setFont(qcombobox_font())
        self.world_select.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.world_select.setGraphicsEffect(get_shadow(30))

        self.right_eye_label = QtWidgets.QLabel()
        self.right_eye_label.setFont(text_font())
        self.right_eye_label.setStyleSheet(QLabel_device)

        self.left_eye_label = QtWidgets.QLabel()
        self.left_eye_label.setFont(text_font())
        self.left_eye_label.setStyleSheet(QLabel_device)

        self.world_label = QtWidgets.QLabel()
        self.world_label.setFont(text_font())
        self.world_label.setStyleSheet(QLabel_device)

        self.status_label = QtWidgets.QLabel()
        self.status_label.setObjectName("statusLabel")
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.status_label.setFont(text_font())
        self.status_label.setStyleSheet("color: rgb(56, 65, 157);")
        self.status_label.setFixedHeight(30)
        self.status_label.setWordWrap(True)

        self.refresh_devices_button = QtWidgets.QPushButton()
        self.refresh_devices_button.setFont(text_font())
        self.refresh_devices_button.setObjectName("refresh_devices_button")
        self.refresh_devices_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.refresh_devices_button.setStyleSheet(QRefreshButton)
        self.refresh_devices_button.setFixedWidth(180)
        self.refresh_devices_button.clicked.connect(self.refresh_devices)

        self.right_eye_preview_button = QtWidgets.QPushButton()
        self.right_eye_preview_button.setFont(text_font())
        self.right_eye_preview_button.setObjectName("right_eye_preview_button")
        self.right_eye_preview_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.right_eye_preview_button.setStyleSheet(QDevicePreviewButton)
        self.right_eye_preview_button.setFixedWidth(180)
        self.right_eye_preview_button.clicked.connect(self.toggle_right_preview)
        self.right_eye_preview_button.setGraphicsEffect(get_shadow(30))

        self.left_eye_preview_button = QtWidgets.QPushButton()
        self.left_eye_preview_button.setFont(text_font())
        self.left_eye_preview_button.setObjectName("left_eye_preview_button")
        self.left_eye_preview_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.left_eye_preview_button.setStyleSheet(QDevicePreviewButton)
        self.left_eye_preview_button.clicked.connect(self.toggle_left_preview)
        self.left_eye_preview_button.setGraphicsEffect(get_shadow(30))

        self.world_preview_button = QtWidgets.QPushButton()
        self.world_preview_button.setFont(text_font())
        self.world_preview_button.setObjectName("world_preview_button")
        self.world_preview_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.world_preview_button.setStyleSheet(QDevicePreviewButton)
        self.world_preview_button.clicked.connect(self.toggle_world_preview)
        self.world_preview_button.setGraphicsEffect(get_shadow(30))

        self.frame_center_layout.addWidget(self.right_eye_label, 0, 0)
        self.frame_center_layout.addWidget(self.right_eye_select, 0, 1)
        self.frame_center_layout.addWidget(self.left_eye_label, 1, 0)
        self.frame_center_layout.addWidget(self.left_eye_select, 1, 1)
        self.frame_center_layout.addWidget(self.world_label, 2, 0)
        self.frame_center_layout.addWidget(self.world_select, 2, 1)
        self.frame_center_layout.addWidget(self.status_label, 3, 1, 1, 2)
        self.frame_center_layout.addWidget(self.refresh_devices_button, 3, 3, 1, 1)

        self.frame_center_layout.addWidget(self.right_eye_preview_button, 0, 3)
        self.frame_center_layout.addWidget(self.left_eye_preview_button, 1, 3)
        self.frame_center_layout.addWidget(self.world_preview_button, 2, 3)

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

        self.frame_bottom_center_layout = QtWidgets.QHBoxLayout(self.frame_bottom_center)
        self.frame_bottom_center_layout.setObjectName("frame_bottom_center_layout")

        self.save_devices_button = QtWidgets.QPushButton()
        self.save_devices_button.setFont(text_font())
        self.save_devices_button.setObjectName("saveDevicesButton")
        self.save_devices_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.save_devices_button.setFixedHeight(50)
        self.save_devices_button.setStyleSheet(QControlPanelMainButton)
        self.save_devices_button.clicked.connect(self.save_devices)
        self.save_devices_button.setDisabled(False)
        self.save_devices_button.setGraphicsEffect(get_shadow(30))

        self.reset_button = QtWidgets.QPushButton()
        self.reset_button.setFont(text_font())
        self.reset_button.setObjectName("reset_button")
        self.reset_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.reset_button.setFixedSize(150, 50)
        self.reset_button.setStyleSheet(QControlPanelButton)
        self.reset_button.clicked.connect(self.reset_devices)
        self.reset_button.setGraphicsEffect(get_shadow(30))

        self.calibrate_device_button = QtWidgets.QPushButton()
        self.calibrate_device_button.setFont(text_font())
        self.calibrate_device_button.setObjectName("calibrateDeviceButton")
        self.calibrate_device_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.calibrate_device_button.setFixedHeight(50)
        self.calibrate_device_button.setStyleSheet(QControlPanelMainButton)
        self.calibrate_device_button.setDisabled(True)
        self.calibrate_device_button.clicked.connect(self.calibrate_device)
        self.calibrate_device_button.setGraphicsEffect(get_shadow(30))

        self.frame_bottom_center_layout.addWidget(self.save_devices_button)
        self.frame_bottom_center_layout.addWidget(self.reset_button)
        self.frame_bottom_center_layout.addWidget(self.calibrate_device_button)

        self.gridLayout.addWidget(self.frame_bottom_center, 2, 1, 1, 4)

        # Bottom Right Frame
        self.frame_bottom_right = QtWidgets.QFrame(self)
        self.frame_bottom_right.setStyleSheet("")
        self.frame_bottom_right.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_bottom_right.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_bottom_right.setObjectName("frame_bottom_right")
        self.frame_bottom_right.setFixedWidth(100)
        self.gridLayout.addWidget(self.frame_bottom_right, 2, 5, 1, 1)

        if Devices.RIGHT_EYE_DEVICE and Devices.LEFT_EYE_DEVICE and Devices.WORLD_DEVICE:
            self.calibrate_device_button.setDisabled(False)
            self.save_devices_button.setDisabled(True)

        self.fill_device_selects()

        self.retranslate_ui()

    def retranslate_ui(self) -> None:
        _translate = QtCore.QCoreApplication.translate

        self.calibrationLabel.setText(_translate("DeviceScreen", "DEVICES"))
        self.right_eye_label.setText(_translate("DeviceScreen", "Right eye device:"))
        self.left_eye_label.setText(_translate("DeviceScreen", "Left eye device:"))
        self.world_label.setText(_translate("DeviceScreen", "World device:"))
        self.save_devices_button.setText(_translate("DeviceScreen", "Save devices"))
        self.reset_button.setText(_translate("DeviceScreen", "Reset"))
        self.calibrate_device_button.setText(_translate("DeviceScreen", "Calibrate a device"))
        self.refresh_devices_button.setText(_translate("DeviceScreen", "Refresh"))

        self.right_eye_preview_button.setText(_translate("DeviceScreen", "Start preview"))
        self.left_eye_preview_button.setText(_translate("DeviceScreen", "Start preview"))
        self.world_preview_button.setText(_translate("DeviceScreen", "Start preview"))

    def switch_to_main(self) -> None:
        self.stacked_widget.setCurrentIndex(0)

    def save_devices(self) -> None:
        _translate = QtCore.QCoreApplication.translate

        if '' in [self.right_eye_select.currentText(),
                  self.left_eye_select.currentText(),
                  self.world_select.currentText()]:
            self.status_label.setText("All fields need to be filled")
            QtCore.QTimer.singleShot(2000, self.clear_label)
            return

        Devices.RIGHT_EYE_DEVICE = Devices.Device(self.right_eye_select.currentText(), "right")
        Devices.LEFT_EYE_DEVICE = Devices.Device(self.left_eye_select.currentText(), "left")
        Devices.WORLD_DEVICE = Devices.Device(self.world_select.currentText(), "world")

        if not Devices.RIGHT_EYE_DEVICE.supported:
            self.device_not_supported_alert("right eye")
        elif not Devices.LEFT_EYE_DEVICE.supported:
            self.device_not_supported_alert("left eye")
        elif not Devices.WORLD_DEVICE.supported:
            self.device_not_supported_alert("world")
        else:
            self.right_eye_select.setStyleSheet(QComboBox_selected)
            self.left_eye_select.setStyleSheet(QComboBox_selected)
            self.world_select.setStyleSheet(QComboBox_selected)
            self.status_label.setText("Devices saved successfully")
            self.calibrate_device_button.setDisabled(False)
            self.save_devices_button.setDisabled(True)
            QtCore.QTimer.singleShot(2000, self.clear_label)
            # Devices.WORLD_DEVICE.print_self()
            # Devices.RIGHT_EYE_DEVICE.print_self()
            # Devices.LEFT_EYE_DEVICE.print_self()
            return

    def clear_label(self) -> None:
        self.status_label.setText("")

    def reset_devices(self) -> None:
        Devices.RIGHT_EYE_DEVICE = None
        Devices.LEFT_EYE_DEVICE = None
        Devices.WORLD_DEVICE = None

        self.calibrate_device_button.setDisabled(True)
        self.save_devices_button.setDisabled(False)

    def refresh_devices(self) -> None:
        self.fill_device_selects()
        self.save_devices_button.setDisabled(False)

    def fill_device_selects(self):
        self.check_device_list()

        self.right_eye_select.clear()
        self.left_eye_select.clear()
        self.world_select.clear()

        for device in uvc.device_list():
            self.right_eye_select.addItem(device["name"])
            self.left_eye_select.addItem(device["name"])
            self.world_select.addItem(device["name"])

    def toggle_right_preview(self) -> None:
        if self.right_eye_select.currentText() == '':
            self.status_label.setText("No selected right eye device")
            return

        if not Devices.Device(self.right_eye_select.currentText(), "right").supported:
            self.device_not_supported_alert("right eye")
            return

        if not self.device_preview:
            self.left_eye_preview_button.setDisabled(True)
            self.world_preview_button.setDisabled(True)
            self.right_eye_preview_button.setText("Stop preview")
            self.device_preview = DevicePreview(Devices.Device(self.right_eye_select.currentText(), "right"))
            self.device_preview.start()
        else:
            self.device_preview.stop()
            self.device_preview = None
            self.left_eye_preview_button.setDisabled(False)
            self.world_preview_button.setDisabled(False)
            self.right_eye_preview_button.setText("Start preview")

    def toggle_left_preview(self) -> None:
        if self.left_eye_select.currentText() == '':
            self.status_label.setText("No selected left eye device")
            return

        if not Devices.Device(self.left_eye_select.currentText(), "left").supported:
            self.device_not_supported_alert("left eye")
            return

        if not self.device_preview:
            self.right_eye_preview_button.setDisabled(True)
            self.world_preview_button.setDisabled(True)
            self.left_eye_preview_button.setText("Stop preview")
            self.device_preview = DevicePreview(Devices.Device(self.left_eye_select.currentText(), "left"))
            self.device_preview.start()
        else:
            self.device_preview.stop()
            self.device_preview = None
            self.right_eye_preview_button.setDisabled(False)
            self.world_preview_button.setDisabled(False)
            self.left_eye_preview_button.setText("Start preview")

    def toggle_world_preview(self) -> None:
        if self.world_select.currentText() == '':
            self.status_label.setText("No selected world eye device")
            return

        if not Devices.Device(self.world_select.currentText(), "world").supported:
            self.device_not_supported_alert("world")
            return

        if not self.device_preview:
            self.right_eye_preview_button.setDisabled(True)
            self.left_eye_preview_button.setDisabled(True)
            self.world_preview_button.setText("Stop preview")
            self.device_preview = DevicePreview(Devices.Device(self.world_select.currentText(), "world"))
            self.device_preview.start()
        else:
            self.device_preview.stop()
            self.device_preview = None
            self.right_eye_preview_button.setDisabled(False)
            self.left_eye_preview_button.setDisabled(False)
            self.world_preview_button.setText("Start preview")

    def device_not_supported_alert(self, device_type) -> None:
        self.status_label.setText("Selected " + device_type + " device is not supported, please edit CONFIG.json")
        QtCore.QTimer.singleShot(2000, self.clear_label)
        return

    def calibrate_device(self) -> None:
        ...

    def check_device_list(self):
        if not uvc.device_list():
            self.status_label.setText("No connected devices available")
            self.right_eye_select.clear()
            self.left_eye_select.clear()
            self.world_select.clear()
            QtCore.QTimer.singleShot(2000, self.clear_label)
            return
