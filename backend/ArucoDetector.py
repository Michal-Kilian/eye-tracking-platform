import cv2
from backend import Devices
import numpy as np


class ArucoDetector:
    def __init__(self):
        super().__init__()
        self.detector_dictionary = cv2.aruco.getPredefinedDictionary(Devices.ARUCO_TYPE)
        self.detector_parameters = cv2.aruco.DetectorParameters()
        self.aruco_detector = cv2.aruco.ArucoDetector(self.detector_dictionary, self.detector_parameters)
        self.corners = None
        self.ids = None
        self.rejected = None
        self.device = Devices.WORLD_DEVICE
        self.matrix_coefficients = self.device.matrix_coefficients
        self.distortion_coefficients = self.device.distortion_coefficients
        print("device in ArucoDetector:", self.device)
        print("matrix_coeff:", self.matrix_coefficients)
        print("dist_coeff:", self.distortion_coefficients)

    def detect(self, frame):
        frame_gray = frame.gray
        frame_bgr = frame.bgr

        self.corners, self.ids, self.rejected = self.aruco_detector.detectMarkers(image=frame_gray)

        if len(self.corners) > 0:
            for i in range(0, len(self.ids)):

                cv2.aruco.drawDetectedMarkers(frame_bgr, self.corners, self.ids)

                rvec, tvec, marker_points = cv2.aruco.estimatePoseSingleMarkers(
                    self.corners[i],
                    20,
                    self.matrix_coefficients,
                    self.distortion_coefficients
                )

                # print("rvec:", rvec)
                print("tvec:", tvec)

                cv2.drawFrameAxes(frame_bgr, self.matrix_coefficients, self.distortion_coefficients, rvec, tvec, 100)
