import cv2
from Helpers import MathHelpers
from backend import Devices
import numpy as np
from scipy.spatial.transform import Rotation


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
                    return False

                cv2.aruco.drawDetectedMarkers(frame_bgr, self.corners, self.ids)

                rvec, tvec, marker_points = cv2.aruco.estimatePoseSingleMarkers(
                    self.corners[i],
                    34.8,
                    self.matrix_coefficients,
                    self.distortion_coefficients
                )

                tvec_dict[self.ids[i][0]] = tvec.ravel()
                rvec_list.append(rvec.ravel())

                total_rvec += rvec.ravel()
                total_tvec += tvec.ravel()

                cv2.drawFrameAxes(frame_bgr,
                                  self.matrix_coefficients,
                                  self.distortion_coefficients,
                                  rvec,
                                  tvec,
                                  100)

            if len(tvec_dict) != 4:
                # print("2 - not 4 markers detected")
                return False

            average_tvec = total_tvec / 4

            image_points, _ = cv2.projectPoints(
                average_tvec,
                np.zeros(3),
                np.zeros(3),
                self.matrix_coefficients,
                self.distortion_coefficients
            )

            cv2.circle(frame_bgr, image_points.ravel().astype(int), 10, (0, 0, 255), 2)

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

            cv2.drawFrameAxes(frame_bgr,
                              self.matrix_coefficients,
                              self.distortion_coefficients,
                              rvec,
                              average_tvec,
                              100)

            # 796 a dalej
            # from pupil_detectors import Detector2D
            # 2D detector, 3D detector, parametre v configu
            # rotacnu maticu do detectoru len dummy udaje (pozicia 0,0,0, rotacia nulova)

            # returns display rotation vector, display rotation matrix, display center position, display normal
            return rvec, n_rotation_matrix, average_tvec, n_z, frame_bgr
