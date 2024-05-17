from frontend.RecordDetailScreen import UIRecordDetailScreen, format_record_date_time
from PyQt5 import QtCore, QtGui, QtWidgets
from frontend.StyleSheets import Fonts, GlobalStyleSheet, RecordsScreenStyleSheet
from backend import RECORDS


class UIRecordsScreen(QtWidgets.QWidget):
    def __init__(self, application, stacked_widget, previous_location, iteration=None):
        super().__init__()

        self.application = application
        self.stacked_widget = stacked_widget
        self.previous_location = previous_location
        self.iteration = 0
        self.analysis_iteration = iteration

        self.setObjectName("RecordsScreen")
        self.setStyleSheet(GlobalStyleSheet.WidgetBackgroundColor)
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
        self.backButton.setStyleSheet(GlobalStyleSheet.BackAndExitButton)
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

        self.recordsLabel = QtWidgets.QLabel()
        self.recordsLabel.setFont(Fonts.HeadingFont())
        self.recordsLabel.setStyleSheet(GlobalStyleSheet.Heading)
        self.recordsLabel.setLineWidth(1)
        self.recordsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.recordsLabel.setObjectName("recordsLabel")

        self.frame_top_center_layout.addWidget(self.recordsLabel)

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
        self.exitButton.setStyleSheet(GlobalStyleSheet.BackAndExitButton)
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
        self.scroll_area.setStyleSheet(GlobalStyleSheet.ScrollBar)
        self.scroll_area.setAlignment(QtCore.Qt.AlignCenter)
        self.scroll_area.setMaximumWidth(750)

        self.scroll_area_widget = QtWidgets.QWidget()
        self.scroll_area_layout = QtWidgets.QGridLayout(self.scroll_area_widget)

        for record in RECORDS.sorted_records():
            _record_id = record.id

            widget = QtWidgets.QWidget()
            widget.setFixedWidth(700)
            widget.setStyleSheet(RecordsScreenStyleSheet.ItemWidget)
            widget_layout = QtWidgets.QHBoxLayout(widget)

            date_time_label = QtWidgets.QLabel(format_record_date_time(record.timestamp))
            date_time_label.setFont(Fonts.TextFont())
            date_time_label.setFixedWidth(150)
            date_time_label.setAlignment(QtCore.Qt.AlignCenter)

            type_label = QtWidgets.QLabel(record.type.value)
            type_label.setFont(Fonts.TextFont())
            type_label.setAlignment(QtCore.Qt.AlignCenter)

            detail_button = QtWidgets.QPushButton("Details")
            detail_button.setFont(Fonts.TextFont())
            detail_button.setFixedWidth(150)
            detail_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            detail_button.setStyleSheet(RecordsScreenStyleSheet.DetailButton)
            detail_button.clicked.connect(
                lambda checked, record_id=_record_id: self.switch_to_record_detail(record_id))

            widget_layout.addWidget(date_time_label, stretch=1)
            widget_layout.addWidget(type_label, stretch=1)
            widget_layout.addWidget(detail_button, stretch=1)
            self.scroll_area_layout.addWidget(widget)

        if not RECORDS.RECORDS:
            label = QtWidgets.QLabel("No records yet")
            label.setFont(Fonts.TextFont())
            label.setAlignment(QtCore.Qt.AlignCenter)

            self.scroll_area_layout.addWidget(label)

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
        self.frame_bottom_center.setStyleSheet(GlobalStyleSheet.ButtonFrame)
        self.frame_bottom_center.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_bottom_center.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_bottom_center.setObjectName("frame_bottom_center")
        self.gridLayout.addWidget(self.frame_bottom_center, 2, 1, 1, 4)

        # Bottom Right Frame
        self.frame_bottom_right = QtWidgets.QFrame(self)
        self.frame_bottom_right.setStyleSheet(GlobalStyleSheet.NoStyleSheet)
        self.frame_bottom_right.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_bottom_right.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_bottom_right.setObjectName("frame_bottom_right")
        self.frame_bottom_right.setFixedWidth(100)
        self.gridLayout.addWidget(self.frame_bottom_right, 2, 5, 1, 1)

        self.retranslate_ui()

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate

        self.recordsLabel.setText(_translate("RecordsScreen", "RECORDS"))

    def back(self):
        if self.previous_location == "analysis":
            self.stacked_widget.setCurrentIndex(self.stacked_widget.currentIndex() - self.analysis_iteration)
        elif self.previous_location == "home":
            self.stacked_widget.setCurrentIndex(0)

    def switch_to_record_detail(self, record_id):
        if self.analysis_iteration:
            self.iteration += 1
            record_detail_screen = UIRecordDetailScreen(self.application, self.stacked_widget, record_id,
                                                        self.iteration)
            self.stacked_widget.addWidget(record_detail_screen)
            self.stacked_widget.setCurrentWidget(record_detail_screen)
