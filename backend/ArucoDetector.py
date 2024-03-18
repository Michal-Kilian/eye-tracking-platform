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
        self.matrix_coefficients = np.array(((933.15867, 0, 657.59), (0, 933.1586, 400.36993), (0, 0, 1)))
        self.distortion_coefficients = np.array((-0.43948, 0.18514, 0, 0))

    def detect(self, frame):
        frame_gray = frame.gray
        frame_bgr = frame.bgr

        self.corners, self.ids, self.rejected = self.aruco_detector.detectMarkers(image=frame_gray)

        if len(self.corners) > 0:
            for i in range(0, len(self.ids)):

                cv2.aruco.drawDetectedMarkers(frame_bgr, self.corners, self.ids)

                rvec, tvec, marker_points = cv2.aruco.estimatePoseSingleMarkers(
                    self.corners[i],
                    0.025,
                    self.matrix_coefficients,
                    self.distortion_coefficients
                )

                # print("rvec:", rvec)
                # print("tvec:", tvec)

                cv2.drawFrameAxes(frame_bgr, self.matrix_coefficients, self.distortion_coefficients, rvec, tvec, 0.1)
