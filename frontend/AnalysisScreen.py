import matplotlib
from PyQt5 import QtCore, QtGui, QtWidgets

import test
from Model3D import Model3D
from backend import Devices
from frontend.RecordsScreen import UIRecordsScreen
from frontend.ArucoOverlay import ArucoOverlay
from frontend.StyleSheets import (QLabel_heading, QBackButton, QButtonFrame,
                                  heading_font, text_font, QWidget_background_color, QControlPanelButton,
                                  QControlPanelMainButton)
from Dialog import Dialog
from test import main

matplotlib.use('Qt5Agg')


class UIAnalysisScreen(QtWidgets.QWidget):
    def __init__(self, application, stacked_widget) -> None:
        super().__init__()

        self.application = application
        self.stacked_widget = stacked_widget
        self.analysis_running = False
        self.overlay = None
        self.picture_selected = None
        self.model_3d = None

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
        self.frame_center_right = QtWidgets.QFrame(self)
        self.frame_center_right.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_center_right.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_center_right.setObjectName("frame_center_right")
        self.frame_center_right.setFixedHeight(370)

        self.frame_center_right_layout = QtWidgets.QGridLayout(self.frame_center_right)

        self.deviceLabel = QtWidgets.QLabel()
        self.deviceLabel.setFont(text_font())
        self.deviceLabel.setLineWidth(1)
        self.deviceLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.deviceLabel.setObjectName("deviceLabel")
        self.deviceLabel.setFixedWidth(252)

        self.deviceStatusLabel = QtWidgets.QLabel()
        self.deviceStatusLabel.setFont(text_font())
        self.deviceStatusLabel.setLineWidth(1)
        self.deviceStatusLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.deviceStatusLabel.setObjectName("deviceStatusLabel")
        self.deviceStatusLabel.setWordWrap(True)
        self.deviceStatusLabel.setStyleSheet("background-color: rgb(56,65,157); color: rgb(255, 255, 255, 95);")
        self.deviceStatusLabel.setFixedWidth(253)

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
        self.picturePathLabel.setStyleSheet("background-color: rgb(56,65,157); color: rgb(255, 255, 255, 95);")
        self.picturePathLabel.setFixedWidth(253)

        self.model_3d = Model3D(10, 10)
        self.model_3d.visualize_graph([(0, -500, 100)], (0, -50, 0), (0, 0, 0),
                                      (0, 50, 1), scale_factor=0.5)

        self.frame_center_right_layout.addWidget(self.model_3d, 0, 0, 2, 1)
        self.frame_center_right_layout.addWidget(self.deviceLabel, 0, 1)
        self.frame_center_right_layout.addWidget(self.deviceStatusLabel, 0, 2)
        self.frame_center_right_layout.addWidget(self.pictureLabel, 1, 1)
        self.frame_center_right_layout.addWidget(self.picturePathLabel, 1, 2)

        self.gridLayout.addWidget(self.frame_center_right, 1, 0, 1, 6)

        # Bottom Center Frame
        self.frame_bottom_center = QtWidgets.QFrame(self)
        self.frame_bottom_center.setStyleSheet(QButtonFrame)
        self.frame_bottom_center.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_bottom_center.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_bottom_center.setObjectName("frame_bottom_center")

        self.frame_bottom_center_layout = QtWidgets.QHBoxLayout(self.frame_bottom_center)

        self.recordsButton = QtWidgets.QPushButton()
        self.recordsButton.setFont(text_font())
        self.recordsButton.setObjectName("recordsButton")
        self.recordsButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.recordsButton.setFixedHeight(50)
        self.recordsButton.setStyleSheet(QControlPanelButton)
        self.recordsButton.clicked.connect(self.switch_to_records)

        self.startButton = QtWidgets.QPushButton()
        self.startButton.setFont(text_font())
        self.startButton.setObjectName("startButton")
        self.startButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.startButton.setFixedHeight(50)
        self.startButton.setStyleSheet(QControlPanelMainButton)
        self.startButton.clicked.connect(self.start_analysis)

        self.loadPictureButton = QtWidgets.QPushButton()
        self.loadPictureButton.setFont(text_font())
        self.loadPictureButton.setObjectName("loadPictureButton")
        self.loadPictureButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.loadPictureButton.setFixedHeight(50)
        self.loadPictureButton.setStyleSheet(QControlPanelButton)
        self.loadPictureButton.clicked.connect(self.load_picture)

        # self.frame_bottom_center_layout.addWidget(self.view3DModelButton)
        self.frame_bottom_center_layout.addWidget(self.recordsButton)
        self.frame_bottom_center_layout.addWidget(self.startButton)
        self.frame_bottom_center_layout.addWidget(self.loadPictureButton)

        self.gridLayout.addWidget(self.frame_bottom_center, 2, 0, 1, 6)

        self.retranslate_ui()

    def retranslate_ui(self) -> None:
        _translate = QtCore.QCoreApplication.translate

        self.analysisLabel.setText(_translate("Form", "ANALYSIS"))
        self.recordsButton.setText(_translate("Form", "Records"))
        self.startButton.setText(_translate("Form", "Start"))
        self.loadPictureButton.setText(_translate("Form", "Load Picture"))

        self.deviceLabel.setText(_translate("Form", "Current world device:"))
        if not Devices.WORLD_DEVICE:
            self.deviceStatusLabel.setStyleSheet("background-color: rgb(56,65,157); color: rgb(255, 255, 255, 95);")
            self.deviceStatusLabel.setText(_translate("Form", "No world device saved yet\n"
                                                              "-> Home -> Devices"))
        else:
            self.deviceStatusLabel.setStyleSheet("background-color: rgb(56,65,157); color: white;")
            self.deviceStatusLabel.setText(_translate("Form", Devices.WORLD_DEVICE.name))

        self.pictureLabel.setText(_translate("Form", "Picture loaded:"))
        if not self.picture_selected:
            self.picturePathLabel.setStyleSheet("background-color: rgb(56,65,157); color: rgb(255, 255, 255, 95);")
            self.picturePathLabel.setText(_translate("Form", "No picture loaded yet\n"
                                                             "-> Load picture"))
        else:
            self.picturePathLabel.setStyleSheet("background-color: rgb(56,65,157); color: white;")
            self.picturePathLabel.setText(_translate("Form", self.picture_selected))

    def start_analysis(self) -> None:
        if not self.analysis_running:
            if not self.picture_selected:
                dlg = Dialog(self.stacked_widget)
                if not dlg.exec():
                    return

            self.overlay = ArucoOverlay()
            self.overlay.showFullScreen()
            self.startButton.setText("Stop")

            test.main()

            self.analysis_running = True
        else:
            self.overlay.close()
            self.startButton.setText("Start")
            self.analysis_running = False

    def switch_to_main(self) -> None:
        self.stacked_widget.setCurrentIndex(0)

    def switch_to_records(self) -> None:
        records_screen = UIRecordsScreen(self.application, self.stacked_widget, "analysis")
        self.stacked_widget.addWidget(records_screen)
        self.stacked_widget.setCurrentWidget(records_screen)

    def load_picture(self) -> None:

        if not self.picture_selected:
            picture, check = QtWidgets.QFileDialog.getOpenFileName(
                None,
                "QFileDialog.getOpenFileName()",
                "",
                "All Files (*);;Python Files (*.py);;Text Files (*.txt)"
            )
            if check:
                self.picture_selected = picture
                self.picturePathLabel.setStyleSheet("background-color: rgb(56,65,157); color: white;")
                self.picturePathLabel.setText(self.picture_selected)
                self.loadPictureButton.setText("Reset picture")
        else:
            self.picture_selected = None
            self.picturePathLabel.setStyleSheet("background-color: rgb(56,65,157); color: rgb(255, 255, 255, 95);")
            self.picturePathLabel.setText("No picture loaded yet\n-> Load picture")
            self.loadPictureButton.setText("Load picture")
