from PyQt5 import QtCore, QtGui, QtWidgets
from pyqt_switch import PyQtSwitch
from frontend.StyleSheets import (QLabel_heading, QBackButton, QButtonFrame,
                                  heading_font, text_font, QWidget_background_color, QControlPanelButton,
                                  QControlPanelMainButton, QLabel_device, QLabel_2D_3D, QScrollBar)


class UIPreferencesScreen(QtWidgets.QWidget):
    def __init__(self, application, stacked_widget) -> None:
        super().__init__()

        self.stacked_widget = stacked_widget

        self.setObjectName("PreferencesScreen")
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

        self.preferencesLabel = QtWidgets.QLabel()
        self.preferencesLabel.setFont(heading_font())
        self.preferencesLabel.setStyleSheet(QLabel_heading)
        self.preferencesLabel.setLineWidth(1)
        self.preferencesLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.preferencesLabel.setObjectName("preferencesLabel")

        self.frame_top_center_layout.addWidget(self.preferencesLabel)

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

        self.detector_2d_label = QtWidgets.QLabel()
        self.detector_2d_label.setFont(text_font())
        self.detector_2d_label.setStyleSheet(QLabel_2D_3D)
        self.detector_2d_label.setFixedHeight(60)
        self.detector_2d_label.setAlignment(QtCore.Qt.AlignCenter)

        self.detector_3d_label = QtWidgets.QLabel()
        self.detector_3d_label.setFont(text_font())
        self.detector_3d_label.setStyleSheet(QLabel_2D_3D)
        self.detector_3d_label.setFixedHeight(60)
        self.detector_3d_label.setAlignment(QtCore.Qt.AlignCenter)

        self.scroll_area_2d = QtWidgets.QScrollArea()
        self.scroll_area_2d.setStyleSheet(QScrollBar)
        self.scroll_area_2d.setAlignment(QtCore.Qt.AlignCenter)
        self.scroll_area_2d.setFixedHeight(250)

        self.scroll_area_3d = QtWidgets.QScrollArea()
        self.scroll_area_3d.setStyleSheet(QScrollBar)
        self.scroll_area_3d.setAlignment(QtCore.Qt.AlignCenter)
        self.scroll_area_3d.setFixedHeight(250)

        self.scroll_area_2d_widget = QtWidgets.QWidget()
        self.scroll_area_3d_widget = QtWidgets.QWidget()

        self.scroll_area_2d_layout = QtWidgets.QGridLayout(self.scroll_area_2d_widget)
        self.scroll_area_3d_layout = QtWidgets.QGridLayout(self.scroll_area_3d_widget)

        self.add_labels_and_input_fields()

        self.scroll_area_2d.setWidget(self.scroll_area_2d_widget)
        self.scroll_area_3d.setWidget(self.scroll_area_3d_widget)

        self.frame_center_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.frame_center_layout.addWidget(self.detector_2d_label, 0, 0)
        self.frame_center_layout.addWidget(self.detector_3d_label, 0, 1)
        self.frame_center_layout.addWidget(self.scroll_area_2d, 1, 0)
        self.frame_center_layout.addWidget(self.scroll_area_3d, 1, 1)

        # self.frame_center_layout.addWidget(self.label1, 2, 0)
        # self.frame_center_layout.addWidget(self.label2, 2, 1)

        # self.frame_center_layout = QtWidgets.QGridLayout(self.frame_center)
        # self.frame_center_layout.setAlignment(QtCore.Qt.AlignCenter)

        # self.language_label = QtWidgets.QLabel()
        # self.language_label.setFont(text_font())
        # self.language_label.setStyleSheet(QLabel_device)
        # self.language_label.setFixedHeight(100)
        # self.language_label.setFixedWidth(200)
        # self.language_label.setAlignment(QtCore.Qt.AlignCenter)

        # self.language = QtWidgets.QLabel()
        # self.language.setFont(text_font())
        # self.language.setStyleSheet(QLabel_device)
        # self.language.setFixedHeight(100)
        # self.language.setFixedWidth(320)
        # self.language.setAlignment(QtCore.Qt.AlignCenter)

        # self.frame_center_layout.addWidget(self.language_label, 0, 0)
        # self.frame_center_layout.addWidget(self.language, 0, 1)
        # self.frame_center_layout.addWidget(self.language_switch, 0, 2)

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

        self.preferencesLabel.setText(_translate("PreferencesScreen", "PREFERENCES"))
        self.detector_2d_label.setText(_translate("PreferencesScreen", "2D Detector parameters"))
        self.detector_3d_label.setText(_translate("PreferencesScreen", "3D Detector parameters"))

    def switch_to_main(self) -> None:
        self.stacked_widget.setCurrentIndex(0)

    def add_labels_and_input_fields(self) -> None:
        for i in range(10):
            label = QtWidgets.QLabel(f"Label {i}")
            label.setFont(text_font())
            input_field = QtWidgets.QLineEdit()
            input_field.setFont(text_font())
            self.scroll_area_2d_layout.addWidget(label, i, 0)
            self.scroll_area_2d_layout.addWidget(input_field, i, 1)

        for i in range(10):
            label = QtWidgets.QLabel(f"Label {i}")
            label.setFont(text_font())
            input_field = QtWidgets.QLineEdit()
            input_field.setFont(text_font())
            self.scroll_area_3d_layout.addWidget(label, i, 0)
            self.scroll_area_3d_layout.addWidget(input_field, i, 1)
