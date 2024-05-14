import os
import threading
import uuid
import cv2
import matplotlib
import uvc
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage
import Model3D
from backend import Devices
from backend import RECORDS
from frontend.GazePointOverlay import GazePointOverlay
from frontend.RecordsScreen import UIRecordsScreen
from frontend.ArucoOverlay import ArucoOverlay
from frontend.StyleSheets import (QLabel_heading, QBackButton, QButtonFrame,
                                  heading_font, text_font, QWidget_background_color, QControlPanelButton,
                                  QControlPanelMainButton, QLabel_Analysis, get_shadow, QScrollBar_Images, QLabel_2D_3D,
                                  QControlButton, QScrollBar)
from frontend.Dialog import Dialog
from backend.Detector2D import Detector2D
from backend.Detector3D import Detector3D
from backend import CONFIG
from backend.Worker import Worker
from backend.ArucoDetector import ArucoDetector
import time

matplotlib.use('agg')


class UIAnalysisScreen(QtWidgets.QWidget):
    def __init__(self, application, stacked_widget) -> None:
        super().__init__()

        self.application = application
        self.stacked_widget = stacked_widget
        self.analysis_running = False
        self.aruco_overlay = None
        self.gaze_point_overlay = None
        self.picture_overlay = None
        self.model_3d_real_time, self.model_3d_offline = None, None
        self.debug_active = None
        (self.worldDeviceLabel, self.worldDeviceStatusLabel, self.rightEyeDeviceLabel, self.rightEyeDeviceStatusLabel,
         self.leftEyeDeviceLabel, self.leftEyeDeviceStatusLabel, self.pictureLabel, self.picturePathLabel,
         self.loadPictureButton, self.debug_right_display, self.debug_left_display, self.debug_world_display,
         self.debug_display) = (None, None, None, None, None, None, None, None, None, None, None, None, None)
        (self.images_scroll_area, self.images_scroll_area_widget, self.images_scroll_area_layout,
         self.image_list_label) = (None, None, None, None)
        self.current_button = None
        self.image_preview, self.image_preview_label = None, None

        self.detector_2d = None
        self.frame_generator = None
        self.detector_3d_right, self.detector_3d_left = None, None
        self.detector_3d_offline = None
        self.aruco_detector = None

        self.threadpool = QtCore.QThreadPool().globalInstance()
        self.right_worker = None
        self.left_worker = None
        self.world_worker = None
        self.analysis_worker = None

        self.right_mutex, self.left_mutex, self.world_mutex = threading.Lock(), threading.Lock(), threading.Lock()
        self.latest_right_frame, self.latest_left_frame, self.latest_world_frame = None, None, None
        self.right_active, self.left_active, self.world_active = False, False, False

        self.iteration = 0

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

        if CONFIG.MODE_SELECTED == RECORDS.RecordType.REAL_TIME:
            self.debug_view = QtWidgets.QScrollArea()
            self.debug_view.setStyleSheet(QScrollBar)
            self.debug_view.setAlignment(QtCore.Qt.AlignCenter)
            self.debug_view_widget = QtWidgets.QWidget()
            self.debug_view_layout = QtWidgets.QGridLayout(self.debug_view_widget)

            self.fill_real_time_debug_view()

            self.debug_view.setWidget(self.debug_view_widget)
        else:
            self.debug_view = QtWidgets.QWidget()
            self.debug_view_layout = QtWidgets.QGridLayout()
            self.debug_view.setLayout(self.debug_view_layout)

            self.fill_offline_debug_view()

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
        if CONFIG.MODE_SELECTED == RECORDS.RecordType.REAL_TIME:
            self.startButton.setDisabled(not Devices.WORLD_DEVICE or not Devices.LEFT_EYE_DEVICE or
                                         not Devices.RIGHT_EYE_DEVICE)
        self.startButton.clicked.connect(self.start_analysis)
        self.startButton.setGraphicsEffect(get_shadow(30))

        self.toggle_aruco_button = QtWidgets.QPushButton()
        self.toggle_aruco_button.setFont(text_font())
        self.toggle_aruco_button.setObjectName("toggle_aruco_button")
        self.toggle_aruco_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.toggle_aruco_button.setFixedHeight(50)
        self.toggle_aruco_button.setStyleSheet(QControlPanelButton)
        self.toggle_aruco_button.setGraphicsEffect(get_shadow(30))

        if CONFIG.MODE_SELECTED == RECORDS.RecordType.REAL_TIME:
            self.toggle_aruco_button.setText("Show Aruco")
            self.toggle_aruco_button.clicked.connect(self.toggle_aruco_overlay)
        else:
            self.toggle_aruco_button.setText("Records")
            self.toggle_aruco_button.clicked.connect(self.switch_to_records)

        # self.frame_bottom_center_layout.addWidget(self.view3DModelButton)
        self.frame_bottom_center_layout.addWidget(self.debugViewButton)
        self.frame_bottom_center_layout.addWidget(self.startButton)
        self.frame_bottom_center_layout.addWidget(self.toggle_aruco_button)

        self.gridLayout.addWidget(self.frame_bottom_center, 2, 0, 1, 6)

        self.retranslate_ui()

    def retranslate_ui(self) -> None:
        _translate = QtCore.QCoreApplication.translate

        if CONFIG.MODE_SELECTED == RECORDS.RecordType.REAL_TIME:
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
        elif CONFIG.MODE_SELECTED == RECORDS.RecordType.OFFLINE:
            self.analysisLabel.setText(_translate("Form", "OFFLINE ANALYSIS"))
            self.image_list_label.setText(_translate("Form", "List of Images"))
            self.image_preview_label.setText(_translate("Form", "Image Preview"))

        self.debugViewButton.setText(_translate("Form", "Debug View"))
        self.startButton.setText(_translate("Form", "Start"))

    def start_analysis(self) -> None:
        if not self.debug_active:
            self.toggle_debug_view()
        if CONFIG.MODE_SELECTED == RECORDS.RecordType.REAL_TIME:
            if not self.aruco_overlay:
                self.toggle_aruco_overlay()
            if not self.analysis_running:
                if not CONFIG.PICTURE_SELECTED:
                    dlg = Dialog(self.stacked_widget, "No picture chosen", "Continue",
                                 "Cancel", "Are you sure you want to continue without a picture loaded?")
                    if not dlg.exec():
                        return

                self.aruco_overlay = ArucoOverlay()
                self.aruco_overlay.showFullScreen()
                self.gaze_point_overlay = GazePointOverlay()
                self.gaze_point_overlay.showFullScreen()
                self.startButton.setText("Stop")
                self.analysis_running = True

                self.detector_2d = Detector2D()
                self.detector_3d_right = Detector3D(Devices.RIGHT_EYE_DEVICE, "right")
                self.detector_3d_left = Detector3D(Devices.LEFT_EYE_DEVICE, "left")
                self.aruco_detector = ArucoDetector()

                if CONFIG.TEST:
                    self.frame_generator = frame_generator(CONFIG.OFFLINE_MODE_MAX_ID,
                                                           "./" + CONFIG.OFFLINE_MODE_DIRECTORY +
                                                           "/example_{0}.png")

                if not CONFIG.TEST:
                    self.right_worker = Worker(self.right_frame_thread)
                    self.left_worker = Worker(self.left_frame_thread)
                self.world_worker = Worker(self.world_frame_thread)
                self.analysis_worker = Worker(self.real_time_analysis_thread)

                if not CONFIG.TEST:
                    self.threadpool.start(self.right_worker)
                    self.threadpool.start(self.left_worker)
                self.threadpool.start(self.world_worker)
                self.threadpool.start(self.analysis_worker)

                print("Active threads beside Main GUI thread:", self.threadpool.activeThreadCount())

            else:
                self.aruco_overlay.close()
                self.aruco_overlay = None
                self.gaze_point_overlay.close()
                self.gaze_point_overlay = None
                self.toggle_aruco_button.setText("Show Aruco")
                self.stop_real_time_workers()
                self.startButton.setText("Start")
                self.analysis_running = False

        elif CONFIG.MODE_SELECTED == RECORDS.RecordType.OFFLINE:
            if not self.analysis_running:
                self.startButton.setText("Stop")
                self.analysis_running = True

                self.detector_2d = Detector2D()
                self.detector_3d_offline = Detector3D()

                self.frame_generator = frame_generator(CONFIG.OFFLINE_MODE_MAX_ID,
                                                       "./" + CONFIG.OFFLINE_MODE_DIRECTORY +
                                                       "/example_{0}.png")

                self.threadpool = QtCore.QThreadPool()
                worker = Worker(self.offline_analysis_thread)
                self.threadpool.start(worker)

            else:
                self.startButton.setText("Start")
                self.analysis_running = False

    def real_time_analysis_thread(self):
        i = CONFIG.OFFLINE_MODE_MIN_ID
        aruco_displayed = False

        record = RECORDS.Record()
        record.id = uuid.uuid4()
        record.timestamp = time.time()
        record.type = RECORDS.RecordType.REAL_TIME
        record.raw_data = []

        print("STARTING")

        while self.analysis_running:
            if i % CONFIG.OFFLINE_MODE_MAX_ID == 0:
                print("END OF CYCLE")

            if not CONFIG.TEST:
                if not self.latest_right_frame or not self.latest_left_frame or not self.latest_world_frame:
                    continue
            else:
                if not self.latest_world_frame:
                    continue

            # world
            world_frame = self.read_world_frame()
            aruco_detection = self.aruco_detector.detect(world_frame.gray, world_frame.bgr)

            if not aruco_detection:
                display_image(world_frame.bgr, self.debug_world_display)
                # display_image(right_frame_bgr, self.debug_right_display)
                # display_image(left_frame_bgr, self.debug_left_display)
                continue

            if CONFIG.TEST:
                left_frame_bgr = next(self.frame_generator)
                right_frame_bgr = cv2.flip(src=left_frame_bgr, flipCode=1)
                left_frame_gray = cv2.cvtColor(left_frame_bgr, cv2.COLOR_BGR2GRAY)
                right_frame_gray = cv2.cvtColor(right_frame_bgr, cv2.COLOR_BGR2GRAY)
            else:
                right_frame = self.read_right_frame()
                left_frame = self.read_left_frame()
                left_frame_bgr = left_frame.bgr
                right_frame_bgr = right_frame.bgr
                right_frame_gray = right_frame.gray
                left_frame_gray = left_frame.gray

            display_rotation_wcs, display_rotation_matrix, display_position_wcs, normal_wcs, world_img \
                = aruco_detection
            display_image(world_img, self.debug_world_display)

            if not aruco_displayed:
                print("DISPLAY ROTATION MATRIX")
                print(display_rotation_matrix)
                aruco_displayed = True

            # right eye
            # right_frame = self.read_right_frame()
            right_result_2d, right_frame_gray, right_img = self.detector_2d.detect(right_frame_gray,
                                                                                   right_frame_bgr)
            display_image(right_img, self.debug_right_display)

            right_result_3d, right_eye_pos_world, right_gaze_ray, right_plane_intersection_wcs, \
                right_plane_intersection_local = (
                    self.detector_3d_right.detect(
                        right_result_2d, right_frame_gray,
                        normal_wcs,
                        display_position_wcs,
                        display_rotation_matrix
                    ))

            # left eye
            # left_frame = self.read_left_frame()
            left_result_2d, left_frame_gray, left_img = self.detector_2d.detect(left_frame_gray,
                                                                                left_frame_bgr)
            display_image(left_img, self.debug_left_display)

            left_result_3d, left_eye_pos_world, left_gaze_ray, left_plane_intersection_wcs, \
                left_plane_intersection_local = (
                    self.detector_3d_left.detect(
                        left_result_2d, left_frame_gray,
                        normal_wcs,
                        display_position_wcs,
                        display_rotation_matrix
                    ))

            if not right_result_3d and not left_result_3d:
                i += 1
                continue

            final_uv_coords = get_final_uv_coords(right_result_3d, left_result_3d)

            # print(final_uv_coords)

            self.gaze_point_overlay.update_gaze_point(final_uv_coords[0], final_uv_coords[1])

            # print(right_plane_intersection)

            # record.raw_data.append(list(final_uv_coords))
            """
            model = cv2.cvtColor(Model3D.visualize_raycast_real_time(
                all_rays=record.raw_data,
                raycast_end=final_uv_coords,
                camera_pos=(0, 0, 0),
                camera_target_right=right_eye_pos_world,
                camera_target_left=left_eye_pos_world,
                camera_dirs=CONFIG.OFFLINE_CAMERA_DIRS_WORLD,
                right_gaze_ray,
                left_gaze_ray
                screen_width=CONFIG.DISPLAY_WIDTH,
                screen_height=CONFIG.DISPLAY_HEIGHT,
                ray_number=0),
                cv2.COLOR_BGR2RGB)
            """
            # display_image(model, self.model_3d_real_time)

            i += 1

        print("FINISHED")

    def offline_analysis_thread(self) -> None:
        i = CONFIG.OFFLINE_MODE_MIN_ID

        record = RECORDS.Record()
        record.id = uuid.uuid4()
        record.timestamp = time.time()
        record.type = RECORDS.RecordType.OFFLINE
        record.raw_data = []

        while self.analysis_running:
            if i == CONFIG.OFFLINE_MODE_MAX_ID:
                self.startButton.setText("Start")
                self.analysis_running = False
                RECORDS.append_record(record)

            frame_bgr = next(self.frame_generator)
            frame_gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)

            result_2d, frame_gray, img = self.detector_2d.detect(frame_gray, frame_bgr)
            result_3d, eye_pos_world, gaze_ray = self.detector_3d_offline.detect_offline(result_2d, frame_gray)

            record.raw_data.append(list(result_3d))

            model = cv2.cvtColor(Model3D.visualize_raycast_offline(
                record.raw_data,
                result_3d,
                CONFIG.OFFLINE_CAMERA_POSITION,
                eye_pos_world,
                CONFIG.OFFLINE_CAMERA_DIRS_WORLD,
                gaze_ray,
                screen_width=CONFIG.OFFLINE_DISPLAY_WIDTH,
                screen_height=CONFIG.OFFLINE_DISPLAY_HEIGHT,
                ray_number=0),
                cv2.COLOR_BGR2RGB)
            self.display_point(result_3d)

            display_image(img, self.debug_display)
            display_image(model, self.model_3d_offline)
            i += 1

    def stop_real_time_workers(self):
        self.right_active, self.left_active, self.world_active, self.analysis_running = False, False, False, False
        self.right_worker = None
        self.left_worker = None
        self.world_worker = None
        self.analysis_worker = None

    def switch_to_main(self) -> None:
        self.stacked_widget.setCurrentIndex(0)

    def switch_to_records(self) -> None:
        self.iteration += 1
        records_screen = UIRecordsScreen(self.application, self.stacked_widget, "analysis", self.iteration)
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
        if CONFIG.MODE_SELECTED == RECORDS.RecordType.REAL_TIME:
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

        elif CONFIG.MODE_SELECTED == RECORDS.RecordType.OFFLINE:
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

            files.sort(key=lambda x: int(x[8:-4]))

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

    def display_uv_coords(self, uv_coordinates) -> None:
        # circle_coordinates = (image_pixel_width * uv_coordinates[0], image_pixel_height * uv_coordinates[1])
        # displaynut tieto coords na obrazku/screene
        ...

    def display_point(self, coordinates):
        # ako u rapcana
        ...

    def fill_real_time_debug_view(self) -> None:
        debug_right_display_title = QtWidgets.QLabel("Right Eye Detection")
        debug_right_display_title.setFont(text_font())
        debug_right_display_title.setAlignment(QtCore.Qt.AlignCenter)

        debug_left_display_title = QtWidgets.QLabel("Left Eye Detection")
        debug_left_display_title.setFont(text_font())
        debug_left_display_title.setAlignment(QtCore.Qt.AlignCenter)

        model_3d_title = QtWidgets.QLabel("3D Model")
        model_3d_title.setFont(text_font())
        model_3d_title.setAlignment(QtCore.Qt.AlignCenter)
        model_3d_title.setStyleSheet("margin-top: 30px;")

        aruco_detection_title = QtWidgets.QLabel("Aruco Detection")
        aruco_detection_title.setFont(text_font())
        aruco_detection_title.setAlignment(QtCore.Qt.AlignCenter)
        aruco_detection_title.setStyleSheet("margin-top: 30px;")

        self.debug_right_display = QtWidgets.QLabel("Debug Right Display Label")
        self.debug_right_display.setStyleSheet("margin: 20px")
        self.debug_right_display.setAlignment(QtCore.Qt.AlignCenter)
        pixmap = QtGui.QPixmap("./media/EyeIcon.png")
        self.debug_right_display.setPixmap(pixmap)
        self.debug_right_display.setFixedSize(400, 300)
        self.debug_right_display.setScaledContents(True)

        self.debug_left_display = QtWidgets.QLabel("Debug Left Display Label")
        self.debug_left_display.setStyleSheet("margin: 20px")
        self.debug_left_display.setAlignment(QtCore.Qt.AlignCenter)
        pixmap = QtGui.QPixmap("./media/EyeIcon.png")
        self.debug_left_display.setPixmap(pixmap)
        self.debug_left_display.setFixedSize(400, 300)
        self.debug_left_display.setScaledContents(True)

        self.model_3d_real_time = QtWidgets.QLabel("3D Model Display Label")
        self.model_3d_real_time.setFixedSize(400, 300)
        self.model_3d_real_time.setStyleSheet("margin: 20px; background-color: rgb(194, 217, 255);")
        self.model_3d_real_time.setAlignment(QtCore.Qt.AlignCenter)
        pixmap = QtGui.QPixmap("./media/EyeIcon.png")
        self.model_3d_real_time.setPixmap(pixmap)
        self.model_3d_real_time.setScaledContents(True)

        self.debug_world_display = QtWidgets.QLabel("Debug World Display Label")
        self.debug_world_display.setStyleSheet("margin: 20px")
        self.debug_world_display.setAlignment(QtCore.Qt.AlignCenter)
        pixmap = QtGui.QPixmap("./media/EyeIcon.png")
        self.debug_world_display.setPixmap(pixmap)
        self.debug_world_display.setFixedSize(400, 300)
        self.debug_world_display.setScaledContents(True)

        self.debug_view_layout.addWidget(debug_right_display_title, 0, 0)
        self.debug_view_layout.addWidget(debug_left_display_title, 0, 1)
        self.debug_view_layout.addWidget(self.debug_right_display, 1, 0)
        self.debug_view_layout.addWidget(self.debug_left_display, 1, 1)
        self.debug_view_layout.addWidget(model_3d_title, 2, 0)
        self.debug_view_layout.addWidget(aruco_detection_title, 2, 1)
        self.debug_view_layout.addWidget(self.model_3d_real_time, 3, 0)
        self.debug_view_layout.addWidget(self.debug_world_display, 3, 1)

    def fill_offline_debug_view(self):
        self.model_3d_offline = QtWidgets.QLabel("3D Model Display Label")
        self.model_3d_offline.setFixedSize(400, 300)
        self.model_3d_offline.setStyleSheet("margin: 20px; background-color: rgb(194, 217, 255);")
        self.model_3d_offline.setAlignment(QtCore.Qt.AlignCenter)
        pixmap = QtGui.QPixmap("./media/EyeIcon.png")
        self.model_3d_offline.setPixmap(pixmap)
        self.model_3d_offline.setScaledContents(True)

        model_3d_title = QtWidgets.QLabel("3D Model")
        model_3d_title.setFont(text_font())
        model_3d_title.setAlignment(QtCore.Qt.AlignCenter)

        debug_display_title = QtWidgets.QLabel("Eye Detection")
        debug_display_title.setFont(text_font())
        debug_display_title.setAlignment(QtCore.Qt.AlignCenter)

        self.debug_display = QtWidgets.QLabel("Debug Right Display Label")
        self.debug_display.setFixedSize(400, 300)
        self.debug_display.setStyleSheet("margin: 20px")
        self.debug_display.setAlignment(QtCore.Qt.AlignCenter)
        pixmap = QtGui.QPixmap("./media/EyeIcon.png")
        self.debug_display.setPixmap(pixmap)
        self.debug_display.setScaledContents(True)

        self.debug_view_layout.addWidget(model_3d_title, 0, 1)
        self.debug_view_layout.addWidget(debug_display_title, 0, 2)
        self.debug_view_layout.addWidget(self.model_3d_offline, 1, 1)
        self.debug_view_layout.addWidget(self.debug_display, 1, 2)

    def right_frame_thread(self):
        cap = uvc.Capture(Devices.RIGHT_EYE_DEVICE.uid)
        cap.frame_mode = cap.available_modes[Devices.RIGHT_EYE_DEVICE.mode_index]
        # controls_dict = dict([(c.display_name, c) for c in cap.controls])
        # controls_dict['Auto Focus'].value = Devices.RIGHT_EYE_DEVICE.auto_focus
        # controls_dict['Absolute Focus'].value = Devices.RIGHT_EYE_DEVICE.absolute_focus
        self.right_active = True

        try:
            while self.right_active:
                try:
                    frame = cap.get_frame_robust()
                    if frame:
                        with self.right_mutex:
                            self.latest_right_frame = frame
                except Exception as e:
                    print(f"Error in right_frame_thread: {e}")
                    break
        finally:
            cap.close()
            print("Closing the right cap")

    def read_right_frame(self):
        with self.right_mutex:
            return self.latest_right_frame

    def left_frame_thread(self):
        cap = uvc.Capture(Devices.LEFT_EYE_DEVICE.uid)
        cap.frame_mode = cap.available_modes[Devices.LEFT_EYE_DEVICE.mode_index]
        # controls_dict = dict([(c.display_name, c) for c in cap.controls])
        # controls_dict['Auto Focus'].value = Devices.LEFT_EYE_DEVICE.auto_focus
        # controls_dict['Absolute Focus'].value = Devices.LEFT_EYE_DEVICE.absolute_focus
        self.left_active = True

        try:
            while self.left_active:
                try:
                    frame = cap.get_frame_robust()
                    if frame:
                        with self.left_mutex:
                            self.latest_left_frame = frame
                except Exception as e:
                    print(f"Error in left_frame_thread: {e}")
                    break
        finally:
            cap.close()
            print("Closing the left cap")

    def read_left_frame(self):
        with self.left_mutex:
            return self.latest_left_frame

    def world_frame_thread(self):
        cap = uvc.Capture(Devices.WORLD_DEVICE.uid)
        cap.frame_mode = cap.available_modes[Devices.WORLD_DEVICE.mode_index]
        controls_dict = dict([(c.display_name, c) for c in cap.controls])
        controls_dict['Auto Focus'].value = Devices.WORLD_DEVICE.auto_focus
        controls_dict['Absolute Focus'].value = Devices.WORLD_DEVICE.absolute_focus
        self.world_active = True

        try:
            while self.world_active:
                try:
                    frame = cap.get_frame_robust()
                    if frame:
                        with self.world_mutex:
                            self.latest_world_frame = frame
                except Exception as e:
                    print(f"Error in world_frame_thread: {e}")
                    break
        finally:
            cap.close()
            cap = None
            print("Closing the world cap")

    def read_world_frame(self):
        with self.world_mutex:
            return self.latest_world_frame

    def toggle_aruco_overlay(self):
        if self.aruco_overlay is not None:
            self.aruco_overlay.close()
            self.aruco_overlay = None
            self.toggle_aruco_button.setText("Show Aruco")
        else:
            self.aruco_overlay = ArucoOverlay()
            self.aruco_overlay.showFullScreen()
            self.toggle_aruco_button.setText("Hide Aruco")


def display_image(img, label):
    qformat = QImage.Format_Indexed8

    if len(img.shape) == 3:
        if img.shape[2] == 4:
            qformat = QImage.Format_RGBA8888
        else:
            qformat = QImage.Format_RGB888

    out_image = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
    out_image = out_image.rgbSwapped()
    label.setPixmap(QtGui.QPixmap.fromImage(out_image))
    label.setScaledContents(True)


def frame_generator(max_id: int, path_format: str):
    num = 0
    while True:
        yield cv2.imread(path_format.format(num))
        num = (num + 1) % (max_id + 1)


def get_final_uv_coords(right_result_3d, left_result_3d):
    if not right_result_3d:
        final_uv_coords = left_result_3d
    elif not left_result_3d:
        final_uv_coords = right_result_3d
    else:
        final_uv_coords = ((right_result_3d[0] + left_result_3d[0]) / 2,
                           (right_result_3d[1] + left_result_3d[1]) / 2)
    return final_uv_coords
