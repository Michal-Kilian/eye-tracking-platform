from PyQt5 import QtCore, QtGui, QtWidgets

from RecordsScreen import UIRecordsScreen
from frontend.ArucoOverlay import ArucoOverlay
from frontend.StyleSheets import (QLabel_heading, QBackButton, QButtonFrame,
                                  heading_font, text_font, QWidget_background_color, QControlPanelButton,
                                  QControlPanelMainButton)


class UIAnalysisScreen(QtWidgets.QWidget):
    def __init__(self, application, stacked_widget) -> None:
        super().__init__()

        self.stacked_widget = stacked_widget
        self.overlay = None
        self.picture_selected = None
        self.records_screen = UIRecordsScreen(application, stacked_widget)

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
        self.frame_center = QtWidgets.QFrame(self)
        self.frame_center.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_center.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_center.setObjectName("frame_center")
        self.frame_center.setFixedHeight(370)
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
        self.startButton.clicked.connect(self.toggle_overlay)

        self.loadPictureButton = QtWidgets.QPushButton()
        self.loadPictureButton.setFont(text_font())
        self.loadPictureButton.setObjectName("loadPictureButton")
        self.loadPictureButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.loadPictureButton.setFixedHeight(50)
        self.loadPictureButton.setStyleSheet(QControlPanelButton)
        self.loadPictureButton.clicked.connect(self.load_picture)

        self.frame_bottom_center_layout.addWidget(self.recordsButton)
        self.frame_bottom_center_layout.addWidget(self.startButton)
        self.frame_bottom_center_layout.addWidget(self.loadPictureButton)

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

        self.analysisLabel.setText(_translate("Form", "ANALYSIS"))
        self.recordsButton.setText(_translate("Form", "Records"))
        self.startButton.setText(_translate("Form", "Start"))
        self.loadPictureButton.setText(_translate("Form", "Load Picture"))

    def toggle_overlay(self) -> None:
        _translate = QtCore.QCoreApplication.translate

        if self.overlay is None or not self.overlay.isVisible():
            self.overlay = ArucoOverlay()
            self.overlay.showFullScreen()
            self.startButton.setText(_translate("Form", "Stop"))
        else:
            self.overlay.close()
            self.startButton.setText(_translate("Form", "Start"))

    def switch_to_main(self) -> None:
        self.stacked_widget.setCurrentIndex(0)

    def switch_to_records(self) -> None:
        self.stacked_widget.addWidget(self.records_screen)
        self.stacked_widget.setCurrentWidget(self.records_screen)

    def load_picture(self) -> None:
        picture, check = QtWidgets.QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()",
                                                               "",
                                                               "All Files (*);;Python Files (*.py);;Text Files (*.txt)")
        if check:
            self.picture_selected = picture
