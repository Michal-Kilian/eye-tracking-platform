from PyQt5 import QtCore, QtGui, QtWidgets
from backend import CONFIG
from frontend.Dialog import Dialog
from frontend.StyleSheets import (QLabel_heading, QBackButton, QButtonFrame,
                                  heading_font, text_font, QWidget_background_color, QControlPanelButton,
                                  QControlPanelMainButton, QLabel_device, QLabel_2D_3D, QScrollBar, get_shadow)


class UIPreferencesScreen(QtWidgets.QWidget):
    def __init__(self, application, stacked_widget) -> None:
        super().__init__()

        self.stacked_widget = stacked_widget
        self.initial_2d_parameters = {}
        self.initial_3d_parameters = {}

        (self.coarse_detection_le, self.coarse_filter_min_le, self.coarse_filter_max_le, self.intensity_range_le,
         self.blur_size_le, self.canny_threshold_le, self.canny_ration_le, self.canny_aperture_le,
         self.pupil_size_max_le, self.pupil_size_min_le, self.strong_perimeter_ratio_range_min_le,
         self.strong_perimeter_ratio_range_max_le, self.strong_area_ratio_range_min_le,
         self.strong_area_ratio_range_max_le, self.contour_size_min_le, self.ellipse_roundness_ratio_le,
         self.initial_ellipse_fit_threshhold_le, self.final_perimeter_ratio_range_min_le,
         self.final_perimeter_ratio_range_max_le, self.ellipse_true_support_min_dist_le,
         self.support_pixel_ratio_exponent_le) = (None, None, None, None, None, None, None, None, None, None, None,
                                                  None, None, None, None, None, None, None, None, None, None)
        (self.threshold_swirski_le, self.threshold_kalman_le, self.threshold_short_term_le, self.threshold_long_term_le,
         self.long_term_buffer_size_le, self.long_term_forget_time_le, self.long_term_forget_observations_le,
         self.long_term_mode_le, self.model_update_interval_long_term_le, self.model_update_interval_ult_long_term_le,
         self.model_warmup_duration_le, self.calculate_rms_residual_le) = (None, None, None, None, None, None, None,
                                                                           None, None, None, None, None)

        self.setStyleSheet(QWidget_background_color)
        self.gridLayout = QtWidgets.QGridLayout(self)

        # Top Left Frame
        self.frame_top_left = QtWidgets.QFrame(self)
        self.frame_top_left.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_top_left.setFrameShadow(QtWidgets.QFrame.Raised)
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
        self.backButton.clicked.connect(self.switch_to_main)

        self.frame_top_left_layout.addWidget(self.backButton)

        self.gridLayout.addWidget(self.frame_top_left, 0, 0, 1, 1)

        # Top Left Frame 2
        self.frame_top_left_2 = QtWidgets.QFrame(self)
        self.frame_top_left_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_top_left_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.gridLayout.addWidget(self.frame_top_left_2, 0, 1, 1, 1)

        # Top Center Frame
        self.frame_top_center = QtWidgets.QFrame(self)
        self.frame_top_center.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_top_center.setFrameShadow(QtWidgets.QFrame.Raised)

        self.frame_top_center_layout = QtWidgets.QVBoxLayout(self.frame_top_center)
        self.frame_top_center_layout.setAlignment(QtCore.Qt.AlignCenter)

        self.preferencesLabel = QtWidgets.QLabel()
        self.preferencesLabel.setFont(heading_font())
        self.preferencesLabel.setStyleSheet(QLabel_heading)
        self.preferencesLabel.setLineWidth(1)
        self.preferencesLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.frame_top_center_layout.addWidget(self.preferencesLabel)

        self.gridLayout.addWidget(self.frame_top_center, 0, 2, 1, 2)

        # Top Right Frame 2
        self.frame_top_right_2 = QtWidgets.QFrame(self)
        self.frame_top_right_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_top_right_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.gridLayout.addWidget(self.frame_top_right_2, 0, 4, 1, 1)

        # Top Right Frame
        self.frame_top_right = QtWidgets.QFrame(self)
        self.frame_top_right.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_top_right.setFrameShadow(QtWidgets.QFrame.Raised)
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
        self.exitButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.exitButton.clicked.connect(application.exit)

        self.frame_top_right_layout.addWidget(self.exitButton)

        self.gridLayout.addWidget(self.frame_top_right, 0, 5, 1, 1)

        # Center Frame
        self.frame_center = QtWidgets.QFrame(self)
        self.frame_center.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_center.setFrameShadow(QtWidgets.QFrame.Raised)
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

        self.setup_2d_parameters_page()
        self.setup_3d_parameters_page()

        self.scroll_area_2d.setWidget(self.scroll_area_2d_widget)
        self.scroll_area_3d.setWidget(self.scroll_area_3d_widget)

        self.frame_center_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.frame_center_layout.addWidget(self.detector_2d_label, 0, 0)
        self.frame_center_layout.addWidget(self.detector_3d_label, 0, 1)
        self.frame_center_layout.addWidget(self.scroll_area_2d, 1, 0)
        self.frame_center_layout.addWidget(self.scroll_area_3d, 1, 1)

        self.gridLayout.addWidget(self.frame_center, 1, 0, 1, 6)

        # Bottom Left Frame
        self.frame_bottom_left = QtWidgets.QFrame(self)
        self.frame_bottom_left.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_bottom_left.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_bottom_left.setFixedWidth(100)
        self.gridLayout.addWidget(self.frame_bottom_left, 2, 0, 1, 1)

        # Bottom Center Frame
        self.frame_bottom_center = QtWidgets.QFrame(self)
        self.frame_bottom_center.setStyleSheet(QButtonFrame)
        self.frame_bottom_center.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_bottom_center.setFrameShadow(QtWidgets.QFrame.Raised)

        self.frame_bottom_center_layout = QtWidgets.QHBoxLayout(self.frame_bottom_center)

        self.save_changes_button = QtWidgets.QPushButton()
        self.save_changes_button.setFont(text_font())
        self.save_changes_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.save_changes_button.setFixedSize(250, 50)
        self.save_changes_button.setStyleSheet(QControlPanelMainButton)
        self.save_changes_button.setDisabled(True)
        self.save_changes_button.clicked.connect(self.save_changes)
        self.save_changes_button.setGraphicsEffect(get_shadow(30))

        self.reset_button = QtWidgets.QPushButton()
        self.reset_button.setFont(text_font())
        self.reset_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.reset_button.setFixedSize(250, 50)
        self.reset_button.setStyleSheet(QControlPanelButton)
        self.reset_button.clicked.connect(self.reset_to_default)
        self.reset_button.setGraphicsEffect(get_shadow(30))

        self.frame_bottom_center_layout.addWidget(self.save_changes_button)
        self.frame_bottom_center_layout.addWidget(self.reset_button)

        self.gridLayout.addWidget(self.frame_bottom_center, 2, 1, 1, 4)

        # Bottom Right Frame
        self.frame_bottom_right = QtWidgets.QFrame(self)
        self.frame_bottom_right.setStyleSheet("")
        self.frame_bottom_right.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_bottom_right.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_bottom_right.setFixedWidth(100)
        self.gridLayout.addWidget(self.frame_bottom_right, 2, 5, 1, 1)

        self.retranslate_ui()

    def retranslate_ui(self) -> None:
        _translate = QtCore.QCoreApplication.translate

        self.preferencesLabel.setText(_translate("PreferencesScreen", "PREFERENCES"))
        self.detector_2d_label.setText(_translate("PreferencesScreen", "2D Detector Parameters"))
        self.detector_3d_label.setText(_translate("PreferencesScreen", "3D Detector Parameters"))
        self.save_changes_button.setText(_translate("PreferencesScreen", "Save changes"))
        self.reset_button.setText(_translate("PreferencesScreen", "Reset to default"))

    def switch_to_main(self) -> None:
        self.stacked_widget.setCurrentIndex(0)

    def setup_2d_parameters_page(self) -> None:
        if not CONFIG.PARAMETERS_2D:
            parameters_2d: dict = CONFIG.get_2d_default_parameters()
        else:
            parameters_2d: dict = CONFIG.PARAMETERS_2D

        self.initial_2d_parameters = parameters_2d.copy()

        self.coarse_detection_le: QtWidgets.QLineEdit = QtWidgets.QLineEdit()
        self.setup_line_edit(self.coarse_detection_le, parameters_2d.get("coarse_detection"))
        self.coarse_filter_min_le: QtWidgets.QLineEdit = QtWidgets.QLineEdit()
        self.setup_line_edit(self.coarse_filter_min_le, parameters_2d.get("coarse_filter_min"))
        self.coarse_filter_max_le: QtWidgets.QLineEdit = QtWidgets.QLineEdit()
        self.setup_line_edit(self.coarse_filter_max_le, parameters_2d.get("coarse_filter_max"))
        self.intensity_range_le: QtWidgets.QLineEdit = QtWidgets.QLineEdit()
        self.setup_line_edit(self.intensity_range_le, parameters_2d.get("intensity_range"))
        self.blur_size_le: QtWidgets.QLineEdit = QtWidgets.QLineEdit()
        self.setup_line_edit(self.blur_size_le, parameters_2d.get("blur_size"))
        self.canny_threshold_le: QtWidgets.QLineEdit = QtWidgets.QLineEdit()
        self.setup_line_edit(self.canny_threshold_le, parameters_2d.get("canny_threshold"))
        self.canny_ration_le: QtWidgets.QLineEdit = QtWidgets.QLineEdit()
        self.setup_line_edit(self.canny_ration_le, parameters_2d.get("canny_ration"))
        self.canny_aperture_le: QtWidgets.QLineEdit = QtWidgets.QLineEdit()
        self.setup_line_edit(self.canny_aperture_le, parameters_2d.get("canny_aperture"))
        self.pupil_size_max_le: QtWidgets.QLineEdit = QtWidgets.QLineEdit()
        self.setup_line_edit(self.pupil_size_max_le, parameters_2d.get("pupil_size_max"))
        self.pupil_size_min_le: QtWidgets.QLineEdit = QtWidgets.QLineEdit()
        self.setup_line_edit(self.pupil_size_min_le, parameters_2d.get("pupil_size_min"))
        self.strong_perimeter_ratio_range_min_le: QtWidgets.QLineEdit = QtWidgets.QLineEdit()
        self.setup_line_edit(self.strong_perimeter_ratio_range_min_le, parameters_2d.get("strong_perimeter_ratio_"
                                                                                         "range_min"))
        self.strong_perimeter_ratio_range_max_le: QtWidgets.QLineEdit = QtWidgets.QLineEdit()
        self.setup_line_edit(self.strong_perimeter_ratio_range_max_le, parameters_2d.get("strong_perimeter_ratio_"
                                                                                         "range_max"))
        self.strong_area_ratio_range_min_le: QtWidgets.QLineEdit = QtWidgets.QLineEdit()
        self.setup_line_edit(self.strong_area_ratio_range_min_le, parameters_2d.get("strong_area_ratio_range_min"))
        self.strong_area_ratio_range_max_le: QtWidgets.QLineEdit = QtWidgets.QLineEdit()
        self.setup_line_edit(self.strong_area_ratio_range_max_le, parameters_2d.get("strong_area_ratio_range_max"))
        self.contour_size_min_le: QtWidgets.QLineEdit = QtWidgets.QLineEdit()
        self.setup_line_edit(self.contour_size_min_le, parameters_2d.get("contour_size_min"))
        self.ellipse_roundness_ratio_le: QtWidgets.QLineEdit = QtWidgets.QLineEdit()
        self.setup_line_edit(self.ellipse_roundness_ratio_le, parameters_2d.get("ellipse_roundness_ratio"))
        self.initial_ellipse_fit_threshhold_le: QtWidgets.QLineEdit = QtWidgets.QLineEdit()
        self.setup_line_edit(self.initial_ellipse_fit_threshhold_le,
                             parameters_2d.get("initial_ellipse_fit_threshhold"))
        self.final_perimeter_ratio_range_min_le: QtWidgets.QLineEdit = QtWidgets.QLineEdit()
        self.setup_line_edit(self.final_perimeter_ratio_range_min_le, parameters_2d.get("final_perimeter_ratio_"
                                                                                        "range_min"))
        self.final_perimeter_ratio_range_max_le: QtWidgets.QLineEdit = QtWidgets.QLineEdit()
        self.setup_line_edit(self.final_perimeter_ratio_range_max_le, parameters_2d.get("final_perimeter_ratio_"
                                                                                        "range_max"))
        self.ellipse_true_support_min_dist_le: QtWidgets.QLineEdit = QtWidgets.QLineEdit()
        self.setup_line_edit(self.ellipse_true_support_min_dist_le, parameters_2d.get("ellipse_true_support_min_dist"))
        self.support_pixel_ratio_exponent_le: QtWidgets.QLineEdit = QtWidgets.QLineEdit()
        self.setup_line_edit(self.support_pixel_ratio_exponent_le, parameters_2d.get("support_pixel_ratio_exponent"))

        for i in range(len(parameters_2d.keys())):
            parameter_title: QtWidgets.QLabel = QtWidgets.QLabel(f"Label {i}")
            parameter_title.setFont(text_font())
            parameter_title.setFixedWidth(230)
            parameter_title.setText(get_parameter_display_text(list(parameters_2d.keys())[i], i + 1))
            parameter_title.setToolTip(get_parameter_tooltip(list(parameters_2d.keys())[i]))

            self.scroll_area_2d_layout.addWidget(parameter_title, i, 0)
            self.add_2d_line_edits()

    def setup_3d_parameters_page(self) -> None:
        if not CONFIG.PARAMETERS_3D:
            parameters_3d = CONFIG.get_3d_default_parameters()
        else:
            parameters_3d = CONFIG.PARAMETERS_3D

        self.threshold_swirski_le: QtWidgets.QLineEdit = QtWidgets.QLineEdit()
        self.setup_line_edit(self.threshold_swirski_le, parameters_3d.get("threshold_swirski"))
        self.threshold_kalman_le: QtWidgets.QLineEdit = QtWidgets.QLineEdit()
        self.setup_line_edit(self.threshold_kalman_le, parameters_3d.get("threshold_kalman"))
        self.threshold_short_term_le: QtWidgets.QLineEdit = QtWidgets.QLineEdit()
        self.setup_line_edit(self.threshold_short_term_le, parameters_3d.get("threshold_short_term"))
        self.threshold_long_term_le: QtWidgets.QLineEdit = QtWidgets.QLineEdit()
        self.setup_line_edit(self.threshold_long_term_le, parameters_3d.get("threshold_long_term"))
        self.long_term_buffer_size_le: QtWidgets.QLineEdit = QtWidgets.QLineEdit()
        self.setup_line_edit(self.long_term_buffer_size_le, parameters_3d.get("long_term_buffer_size"))
        self.long_term_forget_time_le: QtWidgets.QLineEdit = QtWidgets.QLineEdit()
        self.setup_line_edit(self.long_term_forget_time_le, parameters_3d.get("long_term_forget_time"))
        self.long_term_forget_observations_le: QtWidgets.QLineEdit = QtWidgets.QLineEdit()
        self.setup_line_edit(self.long_term_forget_observations_le, parameters_3d.get("long_term_forget_observations"))
        self.long_term_mode_le: QtWidgets.QLineEdit = QtWidgets.QLineEdit()
        self.setup_line_edit(self.long_term_mode_le, parameters_3d.get("long_term_mode"))
        self.model_update_interval_long_term_le: QtWidgets.QLineEdit = QtWidgets.QLineEdit()
        self.setup_line_edit(self.model_update_interval_long_term_le, parameters_3d.get("model_update_interval_"
                                                                                        "long_term"))
        self.model_update_interval_ult_long_term_le: QtWidgets.QLineEdit = QtWidgets.QLineEdit()
        self.setup_line_edit(self.model_update_interval_ult_long_term_le, parameters_3d.get("model_update_interval_"
                                                                                            "ult_long_term"))
        self.model_warmup_duration_le: QtWidgets.QLineEdit = QtWidgets.QLineEdit()
        self.setup_line_edit(self.model_warmup_duration_le, parameters_3d.get("model_warmup_duration"))
        self.calculate_rms_residual_le: QtWidgets.QLineEdit = QtWidgets.QLineEdit()
        self.setup_line_edit(self.calculate_rms_residual_le, parameters_3d.get("calculate_rms_residual"))

        for i in range(len(parameters_3d.keys())):
            parameter_title: QtWidgets.QLabel = QtWidgets.QLabel(f"Label {i}")
            parameter_title.setFont(text_font())
            parameter_title.setFixedWidth(230)
            parameter_title.setText(get_parameter_display_text(list(parameters_3d.keys())[i], i + 1))
            parameter_title.setToolTip(get_parameter_tooltip(list(parameters_3d.keys())[i]))

            self.scroll_area_3d_layout.addWidget(parameter_title, i, 0)
            self.add_3d_line_edits()

    def add_2d_line_edits(self) -> None:
        self.scroll_area_2d_layout.addWidget(self.coarse_detection_le, 0, 1)
        self.scroll_area_2d_layout.addWidget(self.coarse_filter_min_le, 1, 1)
        self.scroll_area_2d_layout.addWidget(self.coarse_filter_max_le, 2, 1)
        self.scroll_area_2d_layout.addWidget(self.intensity_range_le, 3, 1)
        self.scroll_area_2d_layout.addWidget(self.blur_size_le, 4, 1)
        self.scroll_area_2d_layout.addWidget(self.canny_threshold_le, 5, 1)
        self.scroll_area_2d_layout.addWidget(self.canny_ration_le, 6, 1)
        self.scroll_area_2d_layout.addWidget(self.canny_aperture_le, 7, 1)
        self.scroll_area_2d_layout.addWidget(self.pupil_size_max_le, 8, 1)
        self.scroll_area_2d_layout.addWidget(self.pupil_size_min_le, 9, 1)
        self.scroll_area_2d_layout.addWidget(self.strong_perimeter_ratio_range_min_le, 10, 1)
        self.scroll_area_2d_layout.addWidget(self.strong_perimeter_ratio_range_max_le, 11, 1)
        self.scroll_area_2d_layout.addWidget(self.strong_area_ratio_range_min_le, 12, 1)
        self.scroll_area_2d_layout.addWidget(self.strong_area_ratio_range_max_le, 13, 1)
        self.scroll_area_2d_layout.addWidget(self.contour_size_min_le, 14, 1)
        self.scroll_area_2d_layout.addWidget(self.ellipse_roundness_ratio_le, 15, 1)
        self.scroll_area_2d_layout.addWidget(self.initial_ellipse_fit_threshhold_le, 16, 1)
        self.scroll_area_2d_layout.addWidget(self.final_perimeter_ratio_range_min_le, 17, 1)
        self.scroll_area_2d_layout.addWidget(self.final_perimeter_ratio_range_max_le, 18, 1)
        self.scroll_area_2d_layout.addWidget(self.ellipse_true_support_min_dist_le, 19, 1)
        self.scroll_area_2d_layout.addWidget(self.support_pixel_ratio_exponent_le, 20, 1)

    def add_3d_line_edits(self) -> None:
        self.scroll_area_3d_layout.addWidget(self.threshold_swirski_le, 0, 1)
        self.scroll_area_3d_layout.addWidget(self.threshold_kalman_le, 1, 1)
        self.scroll_area_3d_layout.addWidget(self.threshold_short_term_le, 2, 1)
        self.scroll_area_3d_layout.addWidget(self.threshold_long_term_le, 3, 1)
        self.scroll_area_3d_layout.addWidget(self.long_term_buffer_size_le, 4, 1)
        self.scroll_area_3d_layout.addWidget(self.long_term_forget_time_le, 5, 1)
        self.scroll_area_3d_layout.addWidget(self.long_term_forget_observations_le, 6, 1)
        self.scroll_area_3d_layout.addWidget(self.long_term_mode_le, 7, 1)
        self.scroll_area_3d_layout.addWidget(self.model_update_interval_long_term_le, 8, 1)
        self.scroll_area_3d_layout.addWidget(self.model_update_interval_ult_long_term_le, 9, 1)
        self.scroll_area_3d_layout.addWidget(self.model_warmup_duration_le, 10, 1)
        self.scroll_area_3d_layout.addWidget(self.calculate_rms_residual_le, 11, 1)

    def save_changes(self) -> None:
        self.save_changes_button.setDisabled(True)
        CONFIG.PARAMETERS_2D = self.dictify_2d_line_edits()
        CONFIG.PARAMETERS_3D = self.dictify_3d_line_edits()
        CONFIG.update_config("parameters")

    def reset_to_default(self) -> None:
        dlg = Dialog(self.stacked_widget, "Reset to default", "Yes",
                     "Cancel", "Are you sure you want to reset all parameters to their default values?")
        if not dlg.exec():
            return

        CONFIG.PARAMETERS_2D = CONFIG.get_2d_default_parameters()
        CONFIG.PARAMETERS_3D = CONFIG.get_3d_default_parameters()
        CONFIG.reset_config("parameters")
        self.fill_line_edits()
        self.save_changes_button.setDisabled(True)

    def fill_line_edits(self) -> None:
        self.coarse_detection_le.setText(str(CONFIG.PARAMETERS_2D["coarse_detection"]))
        self.coarse_filter_min_le.setText(str(CONFIG.PARAMETERS_2D["coarse_filter_min"]))
        self.coarse_filter_max_le.setText(str(CONFIG.PARAMETERS_2D["coarse_filter_max"]))
        self.intensity_range_le.setText(str(CONFIG.PARAMETERS_2D["intensity_range"]))
        self.blur_size_le.setText(str(CONFIG.PARAMETERS_2D["blur_size"]))
        self.canny_threshold_le.setText(str(CONFIG.PARAMETERS_2D["canny_threshold"]))
        self.canny_ration_le.setText(str(CONFIG.PARAMETERS_2D["canny_ration"]))
        self.canny_aperture_le.setText(str(CONFIG.PARAMETERS_2D["canny_aperture"]))
        self.pupil_size_max_le.setText(str(CONFIG.PARAMETERS_2D["pupil_size_max"]))
        self.pupil_size_min_le.setText(str(CONFIG.PARAMETERS_2D["pupil_size_min"]))
        self.strong_perimeter_ratio_range_min_le.setText(str(CONFIG.PARAMETERS_2D["strong_perimeter_ratio_"
                                                                                  "range_min"]))
        self.strong_perimeter_ratio_range_max_le.setText(str(CONFIG.PARAMETERS_2D["strong_perimeter_ratio_"
                                                                                  "range_max"]))
        self.strong_area_ratio_range_min_le.setText(str(CONFIG.PARAMETERS_2D["strong_area_ratio_range_min"]))
        self.strong_area_ratio_range_max_le.setText(str(CONFIG.PARAMETERS_2D["strong_area_ratio_range_max"]))
        self.contour_size_min_le.setText(str(CONFIG.PARAMETERS_2D["contour_size_min"]))
        self.ellipse_roundness_ratio_le.setText(str(CONFIG.PARAMETERS_2D["ellipse_roundness_ratio"]))
        self.initial_ellipse_fit_threshhold_le.setText(str(CONFIG.PARAMETERS_2D["initial_ellipse_fit_threshhold"]))
        self.final_perimeter_ratio_range_min_le.setText(str(CONFIG.PARAMETERS_2D["final_perimeter_ratio_"
                                                                                 "range_min"]))
        self.final_perimeter_ratio_range_max_le.setText(str(CONFIG.PARAMETERS_2D["final_perimeter_ratio_"
                                                                                 "range_max"]))
        self.ellipse_true_support_min_dist_le.setText(str(CONFIG.PARAMETERS_2D["ellipse_true_support_min_dist"]))
        self.support_pixel_ratio_exponent_le.setText(str(CONFIG.PARAMETERS_2D["support_pixel_ratio_exponent"]))

        self.threshold_swirski_le.setText(str(CONFIG.PARAMETERS_3D["threshold_swirski"]))
        self.threshold_kalman_le.setText(str(CONFIG.PARAMETERS_3D["threshold_kalman"]))
        self.threshold_short_term_le.setText(str(CONFIG.PARAMETERS_3D["threshold_short_term"]))
        self.threshold_long_term_le.setText(str(CONFIG.PARAMETERS_3D["threshold_long_term"]))
        self.long_term_buffer_size_le.setText(str(CONFIG.PARAMETERS_3D["long_term_buffer_size"]))
        self.long_term_forget_time_le.setText(str(CONFIG.PARAMETERS_3D["long_term_forget_time"]))
        self.long_term_forget_observations_le.setText(str(CONFIG.PARAMETERS_3D["long_term_forget_observations"]))
        self.long_term_mode_le.setText(str(CONFIG.PARAMETERS_3D["long_term_mode"]))
        self.model_update_interval_long_term_le.setText(str(CONFIG.PARAMETERS_3D["model_update_interval_"
                                                                                 "long_term"]))
        self.model_update_interval_ult_long_term_le.setText(str(CONFIG.PARAMETERS_3D["model_update_interval_"
                                                                                     "ult_long_term"]))
        self.model_warmup_duration_le.setText(str(CONFIG.PARAMETERS_3D["model_warmup_duration"]))
        self.calculate_rms_residual_le.setText(str(CONFIG.PARAMETERS_3D["calculate_rms_residual"]))

    def setup_line_edit(self, line_edit: QtWidgets.QLineEdit, value) -> None:
        line_edit.setFont(text_font())
        line_edit.setFixedWidth(100)
        line_edit.setText(str(value))
        line_edit.textEdited.connect(self.check_changes)

    def check_changes(self) -> None:
        self.save_changes_button.setDisabled(False)

    def dictify_2d_line_edits(self) -> dict:
        if None in [self.coarse_detection_le.text(), self.coarse_filter_min_le.text(), self.coarse_filter_max_le.text(),
                    self.intensity_range_le.text(), self.blur_size_le.text(), self.canny_threshold_le.text(),
                    self.canny_ration_le.text(), self.canny_aperture_le.text(), self.pupil_size_max_le.text(),
                    self.pupil_size_min_le.text(), self.strong_perimeter_ratio_range_min_le.text(),
                    self.strong_perimeter_ratio_range_max_le.text(), self.strong_area_ratio_range_min_le.text(),
                    self.strong_area_ratio_range_max_le.text(), self.contour_size_min_le.text(),
                    self.ellipse_roundness_ratio_le.text(), self.initial_ellipse_fit_threshhold_le.text(),
                    self.final_perimeter_ratio_range_min_le.text(), self.final_perimeter_ratio_range_max_le.text(),
                    self.ellipse_true_support_min_dist_le.text(), self.support_pixel_ratio_exponent_le.text()]:
            return {}
        return {
            "coarse_detection": int(self.coarse_detection_le.text() == "True"),
            "coarse_filter_min": int(self.coarse_filter_min_le.text()),
            "coarse_filter_max": int(self.coarse_filter_max_le.text()),
            "intensity_range": int(self.intensity_range_le.text()),
            "blur_size": int(self.blur_size_le.text()),
            "canny_threshold": int(self.canny_threshold_le.text()),
            "canny_ration": int(self.canny_ration_le.text()),
            "canny_aperture": int(self.canny_aperture_le.text()),
            "pupil_size_max": int(self.pupil_size_max_le.text()),
            "pupil_size_min": int(self.pupil_size_min_le.text()),
            "strong_perimeter_ratio_range_min": float(self.strong_perimeter_ratio_range_min_le.text()),
            "strong_perimeter_ratio_range_max": float(self.strong_perimeter_ratio_range_max_le.text()),
            "strong_area_ratio_range_min": float(self.strong_area_ratio_range_min_le.text()),
            "strong_area_ratio_range_max": float(self.strong_area_ratio_range_max_le.text()),
            "contour_size_min": int(self.contour_size_min_le.text()),
            "ellipse_roundness_ratio": float(self.ellipse_roundness_ratio_le.text()),
            "initial_ellipse_fit_threshhold": float(self.initial_ellipse_fit_threshhold_le.text()),
            "final_perimeter_ratio_range_min": float(self.final_perimeter_ratio_range_min_le.text()),
            "final_perimeter_ratio_range_max": float(self.final_perimeter_ratio_range_max_le.text()),
            "ellipse_true_support_min_dist": float(self.ellipse_true_support_min_dist_le.text()),
            "support_pixel_ratio_exponent": float(self.support_pixel_ratio_exponent_le.text())
        }

    def dictify_3d_line_edits(self) -> dict:
        if None in [self.threshold_swirski_le.text(), self.threshold_kalman_le.text(),
                    self.threshold_short_term_le.text(), self.threshold_long_term_le.text(),
                    self.long_term_buffer_size_le.text(), self.long_term_forget_time_le.text(),
                    self.long_term_forget_observations_le.text(), self.long_term_mode_le.text(),
                    self.model_update_interval_long_term_le.text(), self.model_update_interval_ult_long_term_le.text(),
                    self.model_warmup_duration_le.text(), self.calculate_rms_residual_le.text()]:
            return {}
        return {
            "threshold_swirski": float(self.threshold_swirski_le.text()),
            "threshold_kalman": float(self.threshold_kalman_le.text()),
            "threshold_short_term": float(self.threshold_short_term_le.text()),
            "threshold_long_term": float(self.threshold_long_term_le.text()),
            "long_term_buffer_size": int(self.long_term_buffer_size_le.text()),
            "long_term_forget_time": int(self.long_term_forget_time_le.text()),
            "long_term_forget_observations": int(self.long_term_forget_observations_le.text()),
            "long_term_mode": 1 if self.long_term_mode_le.text() == "asynchronous" else 0,
            "model_update_interval_long_term": float(self.model_update_interval_long_term_le.text()),
            "model_update_interval_ult_long_term": float(self.model_update_interval_ult_long_term_le.text()),
            "model_warmup_duration": float(self.model_warmup_duration_le.text()),
            "calculate_rms_residual": int(self.calculate_rms_residual_le.text() == "True")
        }


def get_parameter_display_text(par_title: str, index: int) -> str:
    wrap = 16
    if len(par_title) > wrap:
        return "<span style=\"color: rgb(56, 65, 157);\">" + str(index) + "</span>" + " " + par_title[:wrap] + "..."
    else:
        return "<span style=\"color: rgb(56, 65, 157);\">" + str(index) + "</span>" + " " + par_title


def get_parameter_tooltip(par_title: str) -> str:
    return "<h3>" + par_title + "</h3>"
