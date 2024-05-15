from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets

from PopupWindow import PopupWindow
from backend.Visualization import VisualizationWindow
from frontend.StyleSheets import (QLabel_heading, QBackButton,
                                  heading_font, text_font, QWidget_background_color, QScrollBar,
                                  QControlPanelMainButton, get_shadow, QLabel_Detail)
from backend import RECORDS


class UIRecordDetailScreen(QtWidgets.QWidget):
    def __init__(self, application, stacked_widget, record_id, iteration):
        super().__init__()

        self.application = application
        self.stacked_widget = stacked_widget
        self.record = RECORDS.get_record_from_id(record_id)
        self.iteration = iteration
        self.popup = None

        self.setObjectName("RecordDetailScreen")
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
        self.backButton.clicked.connect(self.back)

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

        self.record_detail_label = QtWidgets.QLabel()
        self.record_detail_label.setFont(heading_font())
        self.record_detail_label.setStyleSheet(QLabel_heading)
        self.record_detail_label.setLineWidth(1)
        self.record_detail_label.setAlignment(QtCore.Qt.AlignCenter)
        self.record_detail_label.setObjectName("record_detail_label")

        self.frame_top_center_layout.addWidget(self.record_detail_label)

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

        self.frame_center_layout = QtWidgets.QVBoxLayout(self.frame_center)
        self.frame_center_layout.setAlignment(QtCore.Qt.AlignCenter)

        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setStyleSheet(QScrollBar)
        self.scroll_area.setAlignment(QtCore.Qt.AlignCenter)
        self.scroll_area.setMaximumWidth(750)

        self.scroll_area_widget = QtWidgets.QWidget()
        self.scroll_area_layout = QtWidgets.QGridLayout(self.scroll_area_widget)

        self.id_label = QtWidgets.QLabel()
        self.id_label.setFont(text_font())
        self.id_label.setAlignment(QtCore.Qt.AlignCenter)
        self.id_label.setStyleSheet("margin-bottom: 30px; background-color: white; padding: 15px; border-radius: 30px;")

        self.type_label_title = QtWidgets.QLabel()
        self.type_label_title.setMinimumWidth(250)
        self.type_label_title.setFont(text_font())
        self.type_label_title.setAlignment(QtCore.Qt.AlignCenter)

        self.type_label = QtWidgets.QLabel()
        self.type_label.setMinimumWidth(250)
        self.type_label.setFont(text_font())
        self.type_label.setAlignment(QtCore.Qt.AlignCenter)
        self.type_label.setStyleSheet(QLabel_Detail)

        self.date_label_title = QtWidgets.QLabel()
        self.date_label_title.setMinimumWidth(250)
        self.date_label_title.setFont(text_font())
        self.date_label_title.setAlignment(QtCore.Qt.AlignCenter)

        self.date_label = QtWidgets.QLabel()
        self.date_label.setMinimumWidth(250)
        self.date_label.setFont(text_font())
        self.date_label.setAlignment(QtCore.Qt.AlignCenter)
        self.date_label.setStyleSheet(QLabel_Detail)

        self.time_label_title = QtWidgets.QLabel()
        self.time_label_title.setMinimumWidth(250)
        self.time_label_title.setFont(text_font())
        self.time_label_title.setAlignment(QtCore.Qt.AlignCenter)

        self.time_label = QtWidgets.QLabel()
        self.time_label.setMinimumWidth(250)
        self.time_label.setFont(text_font())
        self.time_label.setAlignment(QtCore.Qt.AlignCenter)
        self.time_label.setStyleSheet(QLabel_Detail)

        self.debug_display_label = QtWidgets.QLabel("Debug Display Label")
        self.debug_display_label.setFixedWidth(426)
        self.debug_display_label.setFixedHeight(320)
        self.debug_display_label.setStyleSheet("margin: 20px")
        self.debug_display_label.setAlignment(QtCore.Qt.AlignCenter)

        self.control_panel_frame = QtWidgets.QFrame()
        self.control_panel_frame_layout = QtWidgets.QHBoxLayout(self.control_panel_frame)

        self.scroll_area_layout.addWidget(self.id_label, 0, 0, 1, 2)
        self.scroll_area_layout.addWidget(self.type_label_title, 1, 0)
        self.scroll_area_layout.addWidget(self.type_label, 1, 1)
        self.scroll_area_layout.addWidget(self.date_label_title, 2, 0)
        self.scroll_area_layout.addWidget(self.date_label, 2, 1)
        self.scroll_area_layout.addWidget(self.time_label_title, 3, 0)
        self.scroll_area_layout.addWidget(self.time_label, 3, 1)

        self.scroll_area.setWidget(self.scroll_area_widget)

        self.frame_center_layout.addWidget(self.scroll_area)

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
        self.frame_bottom_center.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_bottom_center.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_bottom_center.setObjectName("frame_bottom_center")

        self.frame_bottom_center_layout = QtWidgets.QHBoxLayout(self.frame_bottom_center)

        self.scanpath_button = QtWidgets.QPushButton()
        self.scanpath_button.setFont(text_font())
        self.scanpath_button.setObjectName("generate_scanpath_button")
        self.scanpath_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.scanpath_button.setFixedHeight(50)
        self.scanpath_button.setStyleSheet(QControlPanelMainButton)
        self.scanpath_button.clicked.connect(self.generate_scanpath)
        self.scanpath_button.setGraphicsEffect(get_shadow(30))

        self.heatmap_button = QtWidgets.QPushButton()
        self.heatmap_button.setFont(text_font())
        self.heatmap_button.setObjectName("generate_scanpath_button")
        self.heatmap_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.heatmap_button.setFixedHeight(50)
        self.heatmap_button.setStyleSheet(QControlPanelMainButton)
        self.heatmap_button.clicked.connect(self.generate_heatmap)
        self.heatmap_button.setGraphicsEffect(get_shadow(30))

        self.frame_bottom_center_layout.addWidget(self.scanpath_button)
        self.frame_bottom_center_layout.addWidget(self.heatmap_button)

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

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate

        self.record_detail_label.setText(_translate("RecordDetailScreen", "RECORD DETAIL"))
        self.type_label_title.setText(_translate("RecordDetailScreen", "Type:"))
        self.type_label.setText(_translate("RecordDetailScreen", self.record.type.value))
        self.id_label.setText(_translate("RecordDetailScreen", str(self.record.id)))
        self.date_label_title.setText(_translate("RecordDetailScreen", "Date:"))
        self.date_label.setText(_translate("RecordDetailScreen", format_record_date(self.record.timestamp)))
        self.time_label_title.setText(_translate("RecordDetailScreen", "Time:"))
        self.time_label.setText(_translate("RecordDetailScreen", format_record_time(self.record.timestamp)))
        self.scanpath_button.setText(_translate("RecordDetailScreen", "Generate Scanpath"))
        self.heatmap_button.setText(_translate("RecordDetailScreen", "Generate Heatmap"))

    def back(self):
        self.stacked_widget.setCurrentIndex(self.stacked_widget.currentIndex() - self.iteration)

    def generate_scanpath(self):
        visualization_image = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "Image files (*.jpg "
                                                                                               "*.png *.jpeg)")
        if visualization_image != ('', ''):
            self.popup = VisualizationWindow(visualization_image[0], scanpath=True, raw_data=self.record.raw_data)
            self.popup.show()

    def generate_heatmap(self):
        visualization_image = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "Image files (*.jpg "
                                                                                               "*.png *.jpeg)")
        if visualization_image != ('', ''):
            self.popup = VisualizationWindow(visualization_image[0], heatmap=True, raw_data=self.record.raw_data)
            self.popup.show()


def format_record_date(timestamp) -> str:
    return str(datetime.fromtimestamp(timestamp).strftime("%Y/%m/%d"))


def format_record_time(timestamp) -> str:
    return str(datetime.fromtimestamp(timestamp).strftime("%H:%M:%S"))


def format_record_date_time(timestamp) -> str:
    _date = str(datetime.fromtimestamp(timestamp).strftime("%Y/%m/%d"))
    _time = str(datetime.fromtimestamp(timestamp).strftime("%H:%M:%S"))
    return _date + "<br>" + "<span style='color: rgb(56, 65, 157);'>" + _time + "</span>"
