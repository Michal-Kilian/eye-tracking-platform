import os

import matplotlib
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage

from Model3D import Model3D
from backend import Devices
from frontend.RecordsScreen import UIRecordsScreen
from frontend.ArucoOverlay import ArucoOverlay
from frontend.StyleSheets import (QLabel_heading, QBackButton, QButtonFrame,
                                  heading_font, text_font, QWidget_background_color, QControlPanelButton,
                                  QControlPanelMainButton, QLabel_Analysis, get_shadow, QScrollBar_Images, QLabel_2D_3D,
                                  QControlButton)
from frontend.Dialog import Dialog
from backend.Detector2D import Detector2D
from backend import CONFIG

matplotlib.use('Qt5Agg')


class UIAnalysisScreen(QtWidgets.QWidget):
    def __init__(self, application, stacked_widget) -> None:
        super().__init__()

        self.application = application
        self.stacked_widget = stacked_widget
        self.analysis_running = False
        self.overlay = None
        self.model_3d = None
        self.debug_active = None
        (self.worldDeviceLabel, self.worldDeviceStatusLabel, self.rightEyeDeviceLabel, self.rightEyeDeviceStatusLabel,
         self.leftEyeDeviceLabel, self.leftEyeDeviceStatusLabel, self.pictureLabel, self.picturePathLabel,
         self.loadPictureButton, self.debug_display_label) = \
            (None, None, None, None, None, None, None, None, None, None)
        (self.images_scroll_area, self.images_scroll_area_widget, self.images_scroll_area_layout,
         self.image_list_label) = (None, None, None, None)
        self.current_button = None
        self.image_preview, self.image_preview_label = None, None

        self.test = None
        self.deviceTooltip = "-> Home -> Devices"
        self.loadPictureTooltip = "-> Load Picture"

        self.setObjectName("AnalysisScreen")
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

        self.analysisLabel = QtWidgets.QLabel()
        self.analysisLabel.setFont(heading_font())
        self.analysisLabel.setStyleSheet(QLabel_heading)
        self.analysisLabel.setLineWidth(1)
        self.analysisLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.analysisLabel.setObjectName("analysisLabel")

        self.frame_top_center_layout.addWidget(self.analysisLabel)

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
        self.center_stacked_widget = QtWidgets.QStackedWidget(self)
        self.center_stacked_widget.setFixedHeight(370)

        self.basic_view = QtWidgets.QWidget()
        self.basic_view_layout = QtWidgets.QGridLayout()
        self.basic_view.setLayout(self.basic_view_layout)
        self.fill_basic_view()

        self.debug_view = QtWidgets.QWidget()
        self.debug_view_layout = QtWidgets.QGridLayout()
        self.debug_view.setLayout(self.debug_view_layout)
        self.fill_debug_view()

        self.center_stacked_widget.addWidget(self.basic_view)
        self.center_stacked_widget.addWidget(self.debug_view)

        self.gridLayout.addWidget(self.center_stacked_widget, 1, 0, 1, 6)

        # self.frame_center = QtWidgets.QFrame(self)
        # self.frame_center.setFrameShape(QtWidgets.QFrame.StyledPanel)
        # self.frame_center.setFrameShadow(QtWidgets.QFrame.Raised)
        # self.frame_center.setObjectName("frame_center_right")
        # self.frame_center.setFixedHeight(370)

        # self.frame_center_layout = QtWidgets.QGridLayout(self.frame_center)

        # Bottom Center Frame
        self.frame_bottom_center = QtWidgets.QFrame(self)
        self.frame_bottom_center.setStyleSheet(QButtonFrame)
        self.frame_bottom_center.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_bottom_center.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_bottom_center.setObjectName("frame_bottom_center")

        self.frame_bottom_center_layout = QtWidgets.QHBoxLayout(self.frame_bottom_center)

        self.debugViewButton = QtWidgets.QPushButton()
        self.debugViewButton.setFont(text_font())
        self.debugViewButton.setObjectName("debugViewButton")
        self.debugViewButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.debugViewButton.setFixedHeight(50)
        self.debugViewButton.setStyleSheet(QControlPanelButton)
        self.debugViewButton.clicked.connect(self.toggle_debug_view)
        self.debugViewButton.setGraphicsEffect(get_shadow(30))

        self.startButton = QtWidgets.QPushButton()
        self.startButton.setFont(text_font())
        self.startButton.setObjectName("startButton")
        self.startButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.startButton.setFixedHeight(50)
        self.startButton.setStyleSheet(QControlPanelMainButton)
        if CONFIG.MODE_SELECTED == "real-time":
            self.startButton.setDisabled(not Devices.WORLD_DEVICE or not Devices.LEFT_EYE_DEVICE or
                                         not Devices.RIGHT_EYE_DEVICE)
        self.startButton.clicked.connect(self.start_analysis)
        self.startButton.setGraphicsEffect(get_shadow(30))

        self.recordsButton = QtWidgets.QPushButton()
        self.recordsButton.setFont(text_font())
        self.recordsButton.setObjectName("recordsButton")
        self.recordsButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.recordsButton.setFixedHeight(50)
        self.recordsButton.setStyleSheet(QControlPanelButton)
        self.recordsButton.clicked.connect(self.switch_to_records)
        self.recordsButton.setGraphicsEffect(get_shadow(30))

        # self.frame_bottom_center_layout.addWidget(self.view3DModelButton)
        self.frame_bottom_center_layout.addWidget(self.debugViewButton)
        self.frame_bottom_center_layout.addWidget(self.startButton)
        self.frame_bottom_center_layout.addWidget(self.recordsButton)

        self.gridLayout.addWidget(self.frame_bottom_center, 2, 0, 1, 6)

        self.retranslate_ui()

    def retranslate_ui(self) -> None:
        _translate = QtCore.QCoreApplication.translate

        if CONFIG.MODE_SELECTED == "real-time":
            self.analysisLabel.setText(_translate("Form", "REAL-TIME ANALYSIS"))
            self.worldDeviceLabel.setText(_translate("Form", "World device:"))
            if not Devices.WORLD_DEVICE:
                self.worldDeviceStatusLabel.setStyleSheet("background-color: rgb(165, 195, 255); color: white;")
                self.worldDeviceStatusLabel.setText(_translate("Form", "No world device saved yet"))
            else:
                self.worldDeviceStatusLabel.setStyleSheet(
                    "background-color: rgb(165, 195, 255); color: rgb(25, 32, 80);")
                self.worldDeviceStatusLabel.setText(_translate("Form", Devices.WORLD_DEVICE.name))

            self.rightEyeDeviceLabel.setText(_translate("Form", "Right eye device:"))
            if not Devices.RIGHT_EYE_DEVICE:
                self.rightEyeDeviceStatusLabel.setStyleSheet("background-color: rgb(165, 195, 255); color: white;")
                self.rightEyeDeviceStatusLabel.setText(_translate("Form", "No right eye device saved yet"))
            else:
                self.rightEyeDeviceStatusLabel.setStyleSheet(
                    "background-color: rgb(165, 195, 255); color: rgb(25, 32, 80);")
                self.rightEyeDeviceStatusLabel.setText(_translate("Form", Devices.RIGHT_EYE_DEVICE.name))

            self.leftEyeDeviceLabel.setText(_translate("Form", "Left eye device:"))
            if not Devices.RIGHT_EYE_DEVICE:
                self.leftEyeDeviceStatusLabel.setStyleSheet("background-color: rgb(165, 195, 255); color: white;")
                self.leftEyeDeviceStatusLabel.setText(_translate("Form", "No left eye device saved yet"))
            else:
                self.leftEyeDeviceStatusLabel.setStyleSheet(
                    "background-color: rgb(165, 195, 255); color: rgb(25, 32, 80);")
                self.leftEyeDeviceStatusLabel.setText(_translate("Form", Devices.LEFT_EYE_DEVICE.name))

            self.pictureLabel.setText(_translate("Form", "Picture loaded:"))
            if not CONFIG.PICTURE_SELECTED:
                self.picturePathLabel.setStyleSheet("background-color: rgb(165, 195, 255); color: white;")
                self.picturePathLabel.setText(_translate("Form", "No picture loaded yet"))
                self.loadPictureButton.setText(_translate("Form", "Load Picture"))
            else:
                self.picturePathLabel.setStyleSheet("background-color: rgb(165, 195, 255); rgb(25, 32, 80);")
                self.picturePathLabel.setText(_translate("Form", CONFIG.PICTURE_SELECTED))
                self.loadPictureButton.setText(_translate("Form", "Reset Picture"))
        elif CONFIG.MODE_SELECTED == "offline":
            self.analysisLabel.setText(_translate("Form", "OFFLINE ANALYSIS"))
            self.image_list_label.setText(_translate("Form", "List of Images"))
            self.image_preview_label.setText(_translate("Form", "Image Preview"))

        self.debugViewButton.setText(_translate("Form", "Debug View"))
        self.startButton.setText(_translate("Form", "Start"))
        self.recordsButton.setText(_translate("Form", "Records"))

    def start_analysis(self) -> None:
        if not self.analysis_running:
            if None in [Devices.WORLD_DEVICE, Devices.LEFT_EYE_DEVICE, Devices.RIGHT_EYE_DEVICE]:
                dlg = Dialog(self.stacked_widget, "No picture chosen", "Continue",
                             "Cancel", "Are you sure you want to continue without a picture loaded?")
                if not dlg.exec():
                    return

            self.overlay = ArucoOverlay()
            self.overlay.showFullScreen()
            self.startButton.setText("Stop")

            # self.test = MainTest()
            # self.test.start()

            self.test = Detector2D()
            while self.analysis_running:
                image = self.test.detect()

            self.analysis_running = True
        else:
            self.overlay.close()
            self.startButton.setText("Start")

            self.test.stop()
            self.analysis_running = False

    def switch_to_main(self) -> None:
        self.stacked_widget.setCurrentIndex(0)

    def switch_to_records(self) -> None:
        records_screen = UIRecordsScreen(self.application, self.stacked_widget, "analysis")
        self.stacked_widget.addWidget(records_screen)
        self.stacked_widget.setCurrentWidget(records_screen)

    def load_picture(self) -> None:
        if not CONFIG.PICTURE_SELECTED:
            picture, check = QtWidgets.QFileDialog.getOpenFileName(
                None,
                "QFileDialog.getOpenFileName()",
                "",
                "All Files (*);;Python Files (*.py);;Text Files (*.txt)"
            )
            if check:
                CONFIG.PICTURE_SELECTED = picture
                self.picturePathLabel.setStyleSheet("background-color: rgb(165, 195, 255); color: rgb(25, 32, 80);")
                self.picturePathLabel.setText(CONFIG.PICTURE_SELECTED)
                self.loadPictureButton.setText("Reset picture")
        else:
            CONFIG.PICTURE_SELECTED = None
            self.picturePathLabel.setStyleSheet("background-color: rgb(165, 195, 255); color: white;")
            self.picturePathLabel.setText("No picture loaded yet")
            self.loadPictureButton.setText("Load picture")

    def toggle_debug_view(self):
        if self.debug_active:
            self.center_stacked_widget.setCurrentWidget(self.basic_view)
            self.debugViewButton.setText("Debug View")
            self.debug_active = False
        else:
            self.center_stacked_widget.setCurrentWidget(self.debug_view)
            self.debugViewButton.setText("Basic View")
            self.debug_active = True

    def fill_basic_view(self) -> None:
        if CONFIG.MODE_SELECTED == "real-time":
            self.worldDeviceLabel = QtWidgets.QLabel()
            self.worldDeviceLabel.setFont(text_font())
            self.worldDeviceLabel.setLineWidth(1)
            self.worldDeviceLabel.setAlignment(QtCore.Qt.AlignCenter)
            self.worldDeviceLabel.setObjectName("worldDeviceLabel")
            self.worldDeviceLabel.setFixedWidth(252)

            self.worldDeviceStatusLabel = QtWidgets.QLabel()
            self.worldDeviceStatusLabel.setFont(text_font())
            self.worldDeviceStatusLabel.setLineWidth(1)
            self.worldDeviceStatusLabel.setAlignment(QtCore.Qt.AlignCenter)
            self.worldDeviceStatusLabel.setObjectName("worldDeviceStatusLabel")
            self.worldDeviceStatusLabel.setWordWrap(True)
            self.worldDeviceStatusLabel.setStyleSheet(QLabel_Analysis)
            self.worldDeviceStatusLabel.setFixedWidth(253)

            self.rightEyeDeviceLabel = QtWidgets.QLabel()
            self.rightEyeDeviceLabel.setFont(text_font())
            self.rightEyeDeviceLabel.setLineWidth(1)
            self.rightEyeDeviceLabel.setAlignment(QtCore.Qt.AlignCenter)
            self.rightEyeDeviceLabel.setObjectName("worldDeviceLabel")
            self.rightEyeDeviceLabel.setFixedWidth(252)

            self.rightEyeDeviceStatusLabel = QtWidgets.QLabel()
            self.rightEyeDeviceStatusLabel.setFont(text_font())
            self.rightEyeDeviceStatusLabel.setLineWidth(1)
            self.rightEyeDeviceStatusLabel.setAlignment(QtCore.Qt.AlignCenter)
            self.rightEyeDeviceStatusLabel.setObjectName("worldDeviceStatusLabel")
            self.rightEyeDeviceStatusLabel.setWordWrap(True)
            self.rightEyeDeviceStatusLabel.setStyleSheet(QLabel_Analysis)
            self.rightEyeDeviceStatusLabel.setFixedWidth(253)

            self.leftEyeDeviceLabel = QtWidgets.QLabel()
            self.leftEyeDeviceLabel.setFont(text_font())
            self.leftEyeDeviceLabel.setLineWidth(1)
            self.leftEyeDeviceLabel.setAlignment(QtCore.Qt.AlignCenter)
            self.leftEyeDeviceLabel.setObjectName("worldDeviceLabel")
            self.leftEyeDeviceLabel.setFixedWidth(252)

            self.leftEyeDeviceStatusLabel = QtWidgets.QLabel()
            self.leftEyeDeviceStatusLabel.setFont(text_font())
            self.leftEyeDeviceStatusLabel.setLineWidth(1)
            self.leftEyeDeviceStatusLabel.setAlignment(QtCore.Qt.AlignCenter)
            self.leftEyeDeviceStatusLabel.setObjectName("worldDeviceStatusLabel")
            self.leftEyeDeviceStatusLabel.setWordWrap(True)
            self.leftEyeDeviceStatusLabel.setStyleSheet(QLabel_Analysis)
            self.leftEyeDeviceStatusLabel.setFixedWidth(253)

            self.pictureLabel = QtWidgets.QLabel()
            self.pictureLabel.setFont(text_font())
            self.pictureLabel.setLineWidth(1)
            self.pictureLabel.setAlignment(QtCore.Qt.AlignCenter)
            self.pictureLabel.setObjectName("pictureLabel")
            self.pictureLabel.setFixedWidth(252)

            self.picturePathLabel = QtWidgets.QLabel()
            self.picturePathLabel.setFont(text_font())
            self.picturePathLabel.setLineWidth(1)
            self.picturePathLabel.setAlignment(QtCore.Qt.AlignCenter)
            self.picturePathLabel.setObjectName("picturePathLabel")
            self.picturePathLabel.setWordWrap(True)
            self.picturePathLabel.setStyleSheet(QLabel_Analysis)
            self.picturePathLabel.setFixedWidth(253)

            self.loadPictureButton = QtWidgets.QPushButton()
            self.loadPictureButton.setFont(text_font())
            self.loadPictureButton.setObjectName("loadPictureButton")
            self.loadPictureButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.loadPictureButton.setFixedHeight(50)
            self.loadPictureButton.setStyleSheet(QControlButton)
            self.loadPictureButton.clicked.connect(self.load_picture)
            # self.loadPictureButton.setGraphicsEffect(get_shadow(30))

            self.basic_view_layout.addWidget(self.worldDeviceLabel, 0, 0)
            self.basic_view_layout.addWidget(self.worldDeviceStatusLabel, 0, 1)
            self.basic_view_layout.addWidget(self.rightEyeDeviceLabel, 1, 0)
            self.basic_view_layout.addWidget(self.rightEyeDeviceStatusLabel, 1, 1)
            self.basic_view_layout.addWidget(self.leftEyeDeviceLabel, 2, 0)
            self.basic_view_layout.addWidget(self.leftEyeDeviceStatusLabel, 2, 1)
            self.basic_view_layout.addWidget(self.pictureLabel, 3, 0)
            self.basic_view_layout.addWidget(self.picturePathLabel, 3, 1)
            self.basic_view_layout.addWidget(self.loadPictureButton, 4, 1)

        elif CONFIG.MODE_SELECTED == "offline":
            self.image_list_label = QtWidgets.QLabel()
            self.image_list_label.setFont(text_font())
            self.image_list_label.setStyleSheet(QLabel_2D_3D)
            self.image_list_label.setFixedHeight(60)
            self.image_list_label.setAlignment(QtCore.Qt.AlignCenter)

            self.images_scroll_area = QtWidgets.QScrollArea()
            self.images_scroll_area.setStyleSheet(QScrollBar_Images)
            self.images_scroll_area.setAlignment(QtCore.Qt.AlignCenter)
            self.images_scroll_area.setFixedHeight(250)
            self.images_scroll_area.setFixedWidth(300)

            self.images_scroll_area_widget = QtWidgets.QWidget()
            self.images_scroll_area_layout = QtWidgets.QVBoxLayout(self.images_scroll_area_widget)

            abs_directory = os.path.abspath("./" + CONFIG.OFFLINE_MODE_DIRECTORY)
            if not os.path.exists(abs_directory):
                files = []
                no_files_label = QtWidgets.QLabel("<span style='color: rgba(25, 32, 80, 90)'>No files found in <span "
                                                  "style='color: rgb(56, 65, 157);'><b>images</b></span> "
                                                  "directory.</span>")
                no_files_label.setFont(text_font())
                no_files_label.setWordWrap(True)
                self.images_scroll_area_layout.addWidget(no_files_label)
            else:
                files = os.listdir(abs_directory)

            for _file in files:
                file_button: QtWidgets.QPushButton = QtWidgets.QPushButton(_file)
                file_button.setFont(text_font())
                file_button.setFixedWidth(230)
                file_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                file_button.clicked.connect(
                    lambda checked, file=_file, button=file_button: self.show_image_preview(file, button))
                self.images_scroll_area_layout.addWidget(file_button)

            self.images_scroll_area.setWidget(self.images_scroll_area_widget)

            self.image_preview_label = QtWidgets.QLabel()
            self.image_preview_label.setFont(text_font())
            self.image_preview_label.setStyleSheet(QLabel_2D_3D)
            self.image_preview_label.setFixedHeight(60)
            self.image_preview_label.setAlignment(QtCore.Qt.AlignCenter)

            self.image_preview = QtWidgets.QLabel("Image Preview")
            self.image_preview.setAlignment(QtCore.Qt.AlignCenter)
            self.image_preview.setStyleSheet("background-color: white;")
            self.image_preview.setMaximumSize(300, 200)
            self.image_preview.setFont(text_font())
            pixmap = QtGui.QPixmap("./media/EyeIcon.png")
            self.image_preview.setPixmap(pixmap)
            self.image_preview.setScaledContents(True)

            self.basic_view_layout.addWidget(self.image_list_label, 0, 0)
            self.basic_view_layout.addWidget(self.images_scroll_area, 1, 0)
            self.basic_view_layout.addWidget(self.image_preview_label, 0, 1)
            self.basic_view_layout.addWidget(self.image_preview, 1, 1, 2, 1)

    def show_image_preview(self, file_name, button):
        if self.current_button == button:
            button.setStyleSheet("")
            self.current_button = None
            pixmap = QtGui.QPixmap("./media/EyeIcon.png")
            self.image_preview.setPixmap(pixmap)
            self.image_preview.setScaledContents(True)
            return

        button.setStyleSheet("background-color: rgb(56, 65, 157); color: white;")

        if self.current_button and self.current_button != button:
            self.current_button.setStyleSheet("")

        self.current_button = button

        image_path = os.path.abspath(os.path.join("./images", file_name))
        pixmap = QtGui.QPixmap(image_path)
        if not pixmap.isNull():
            pixmap = pixmap.scaledToWidth(200)
            self.image_preview.setPixmap(pixmap)
            self.image_preview.setScaledContents(True)
        else:
            self.image_preview.setText("<span style='color: '>No preview available</span>")

    def display_image(self, img):
        qformat = QImage.Format_Indexed8

        if len(img.shape) == 3:
            if img.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888

        out_image = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
        out_image = out_image.rgbSwapped()
        self.debug_display_label.setPixmap(QtGui.QPixmap.fromImage(out_image))
        self.debug_display_label.setScaledContents(True)

    def fill_debug_view(self) -> None:
        self.model_3d = Model3D(10, 10)
        self.model_3d.visualize_graph([(0, -500, 100)], (0, -50, 0), (0, 0, 0),
                                      (0, 50, 1), scale_factor=0.5)

        self.debug_display_label = QtWidgets.QLabel("Debug Display Label")
        self.debug_display_label.setFixedWidth(515)
        self.debug_display_label.setStyleSheet("border: 2px solid black; margin: 20px")
        self.debug_display_label.setAlignment(QtCore.Qt.AlignCenter)

        self.debug_view_layout.addWidget(self.model_3d, 0, 0)
        self.debug_view_layout.addWidget(self.debug_display_label, 0, 1)
