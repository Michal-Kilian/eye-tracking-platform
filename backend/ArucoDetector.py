import cv2
import numpy as np
from scipy.spatial.transform import Rotation

from backend import CONFIG
from backend import Devices
from backend.Helpers import MathHelpers


class ArucoDetector:
    def __init__(self, matrix=None, distortion=None):
        super().__init__()
        self.detector_dictionary = cv2.aruco.getPredefinedDictionary(Devices.ARUCO_TYPE)
        self.detector_parameters = cv2.aruco.DetectorParameters()
        self.aruco_detector = cv2.aruco.ArucoDetector(self.detector_dictionary, self.detector_parameters)
        self.corners = None
        self.ids = None
        self.rejected = None
        self.device = Devices.WORLD_DEVICE
        if matrix is None and distortion is None:
            self.matrix_coefficients = self.device.matrix_coefficients
            self.distortion_coefficients = self.device.distortion_coefficients
        else:
            self.matrix_coefficients = matrix
            self.distortion_coefficients = distortion

    def detect(self, frame_gray, frame_bgr):

        self.corners, self.ids, self.rejected = self.aruco_detector.detectMarkers(image=frame_gray)

        if len(self.corners) > 3:
            total_tvec = np.zeros(3)
            total_rvec = np.zeros(3)
            tvec_dict = {}
            rvec_list = []

            for i in range(0, len(self.ids)):
                if self.ids[i][0] > 3:
                    # print("1 - detected other id than 0, 1, 2, 3;", self.ids[i][0])
                    return None, None, None, None, None, None

                # cv2.aruco.drawDetectedMarkers(frame_bgr, self.corners, self.ids)

                rvec, tvec, marker_points = cv2.aruco.estimatePoseSingleMarkers(
                    self.corners[i],
                    CONFIG.MARKER_LENGTH,
                    self.matrix_coefficients,
                    self.distortion_coefficients
                )

                tvec_dict[self.ids[i][0]] = tvec.ravel()
                rvec_list.append(rvec.ravel())

                total_rvec += rvec.ravel()
                total_tvec += tvec.ravel()

                # cv2.drawFrameAxes(frame_bgr,
                #                   self.matrix_coefficients,
                #                   self.distortion_coefficients,
                #                   rvec,
                #                   tvec,
                #                   100)

            if len(tvec_dict) != 4:
                # print("2 - not 4 markers detected")
                return None, None, None, None, None, None

            average_tvec = total_tvec / 4

            image_points, _ = cv2.projectPoints(
                average_tvec,
                np.zeros(3),
                np.zeros(3),
                self.matrix_coefficients,
                self.distortion_coefficients
            )

            # cv2.circle(frame_bgr, image_points.ravel().astype(int), 10, (0, 0, 255), 2)

            avg_1_3 = (tvec_dict[1] + tvec_dict[3]) * 0.5
            avg_0_2 = (tvec_dict[0] + tvec_dict[2]) * 0.5
            x_vector = avg_1_3 - avg_0_2

            avg_0_1 = (tvec_dict[0] + tvec_dict[1]) * 0.5
            avg_2_3 = (tvec_dict[2] + tvec_dict[3]) * 0.5
            y_vector = avg_0_1 - avg_2_3

            n_x = MathHelpers.normalize(x_vector).ravel()
            n_y = MathHelpers.normalize(y_vector).ravel()
            n_z = MathHelpers.normalize(MathHelpers.cross_product(n_x, n_y)).ravel()

            n_rotation_matrix = np.array([[n_x[0], n_y[0], n_z[0]],
                                          [n_x[1], n_y[1], n_z[1]],
                                          [n_x[2], n_y[2], n_z[2]]],
                                         dtype=float)

            # first option
            rvec, _ = cv2.Rodrigues(n_rotation_matrix)

            # second option
            # rvec = Rotation.from_rotvec(rvec_list).mean().as_rotvec()

            # cv2.drawFrameAxes(frame_bgr,
            #                   self.matrix_coefficients,
            #                   self.distortion_coefficients,
            #                   rvec,
            #                   average_tvec,
            #                   100)

            ###
            CONFIG.ARUCO_TEST = True
            corners_from_sub_pix = None
            if CONFIG.ARUCO_TEST:
                nline = CONFIG.CHECKERBOARD_ROWS - 1
                ncol = CONFIG.CHECKERBOARD_COLUMNS - 1
                criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
                ret, corners = cv2.findChessboardCorners(frame_gray, (nline, ncol), None)
                if ret is True:
                    corners_from_sub_pix = cv2.cornerSubPix(frame_gray, corners, (11, 11), (-1, -1), criteria)
                    # cv2.drawChessboardCorners(frame_gray, (nline, ncol), corners_from_sub_pix, ret)

            ###

            return rvec, n_rotation_matrix, average_tvec, n_z, frame_bgr, corners_from_sub_pix
