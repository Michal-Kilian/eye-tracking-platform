import abc
import ctypes
import threading
import uvc
import numpy as np
from backend.Helpers import MathHelpers
from backend.ArucoDetector import ArucoDetector
from backend import CONFIG
import math


class CameraThread(threading.Thread, metaclass=abc.ABCMeta):

    def __init__(self):
        threading.Thread.__init__(self)
        self._scheduledStop = False
        self._frameMutex = threading.Lock()
        self._image = None
        self._newFrame = False
        return

    @property
    def ready(self):
        return self.read(peek=True)[1] is not None

    @property
    @abc.abstractmethod
    def resolution(self):
        return

    @abc.abstractmethod
    def _tinit(self):
        return

    @abc.abstractmethod
    def _tstop(self):
        return

    @abc.abstractmethod
    def _readImage(self):
        return

    def run(self):
        self._tinit()
        while True:
            image = self._readImage()
            if image is not None:
                self._frameMutex.acquire()
                self._image = image
                self._newFrame = True
                self._frameMutex.release()
            if self._scheduledStop:
                self._tstop()
                break
        return

    def stop(self):
        self._scheduledStop = True
        return

    def read(self, peek=False):
        ret = False, None
        self._frameMutex.acquire()
        if self._image is not None:
            ret = self._newFrame, self._image
            if peek is False:
                self._newFrame = False
        self._frameMutex.release()
        return ret


class PyuvcCameraThread(CameraThread):

    def __init__(self, uid, mode_index, controls=None):
        super().__init__()
        if controls is None:
            controls = {}
        self._uid = uid
        self._cap = None
        self._modeIndex = mode_index
        self._controls = controls
        self._allControls = None
        self._resolution = None
        return

    def _tinit(self):
        self._cap = uvc.Capture(self._uid)
        self._cap.frame_mode = self._cap.available_modes[self._modeIndex]
        self._allControls = {c.display_name: c for c in self._cap.controls}

        for key, value in self._controls.items():
            self._allControls[key].value = value
        return

    def _tstop(self):
        self._cap.close()
        return

    @property
    def resolution(self):
        return self._cap.frame_mode.width, self._cap.frame_mode.height

    def _readImage(self):
        frame = None
        try:
            frame = self._cap.get_frame().gray
        except Exception as e:
            print("Could not get frame, reset: " + str(e))
            self._tinit()
        return frame


class PyuvcPoseThread(PyuvcCameraThread):

    def __init__(self, uid, mode_index, controls={}, marker_length=34.8, camera_matrix=np.eye(3),
                 distortion_coeffs=np.zeros(8)):
        super().__init__(uid, mode_index, controls)
        self._arucoDetector = None
        self._markerLength = marker_length
        self._cm = camera_matrix
        self._dcs = distortion_coeffs
        self._poseMutex = threading.Lock()
        self._pose = None, None
        self._image = None
        return

    def _tinit(self):
        import cv2
        super()._tinit()
        detector_dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        detector_parameters = cv2.aruco.DetectorParameters()
        self._arucoDetector = cv2.aruco.ArucoDetector(detector_dictionary, detector_parameters)
        return

    def _getPose(self, image):
        corners, ids, _ = self._arucoDetector.detectMarkers(image)
        if len(corners) > 3:
            total_tvec = np.zeros(3)
            tvec_dict = {}

            for i in range(len(ids)):
                mid = ids[i][0]
                if mid <= 3:
                    rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(
                        corners[i],
                        self._markerLength,
                        self._cm,
                        self._dcs
                    )
                    total_tvec += tvec.ravel()
                    tvec_dict[mid] = tvec.ravel()

                    cv2.aruco.drawDetectedMarkers(image, corners, ids)

                    cv2.drawFrameAxes(image,
                                      self._cm,
                                      self._dcs,
                                      rvec,
                                      tvec,
                                      100)

            if len(tvec_dict) != 4:
                return None, None, image

            image_points, _ = cv2.projectPoints(
                total_tvec / len(total_tvec),
                np.zeros(3),
                np.zeros(3),
                self._cm,
                self._dcs
            )

            cv2.circle(image, image_points.ravel().astype(int), 10, (0, 0, 255), 2)

            avg13 = (tvec_dict[1] + tvec_dict[3]) * 0.5
            avg02 = (tvec_dict[0] + tvec_dict[2]) * 0.5
            x_vec = avg13 - avg02

            avg01 = (tvec_dict[0] + tvec_dict[1]) * 0.5
            avg23 = (tvec_dict[2] + tvec_dict[3]) * 0.5
            y_vec = avg01 - avg23

            nx_vec = MathHelpers.normalize(x_vec).ravel()
            ny_vec = MathHelpers.normalize(y_vec).ravel()
            nz_vec = MathHelpers.normalize(MathHelpers.cross_product(nx_vec, ny_vec)).ravel()

            rot_mat = np.array([
                [nx_vec[0], ny_vec[0], nz_vec[0]],
                [nx_vec[1], ny_vec[1], nz_vec[1]],
                [nx_vec[2], ny_vec[2], nz_vec[2]]]
            )

            rvec, _ = cv2.Rodrigues(rot_mat)

            cv2.drawFrameAxes(image,
                              self._cm,
                              self._dcs,
                              rvec,
                              total_tvec / len(total_tvec),
                              100)

            return rot_mat, total_tvec / len(total_tvec), image

        return None, None, cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

    def _readImage(self):
        frame = super()._readImage()
        if frame is not None:
            pose_rot_mat, pose_center, image = self._getPose(frame)
            if pose_rot_mat is not None:
                self._poseMutex.acquire()
                self._pose = (pose_rot_mat, pose_center)
                self._image = image
                self._poseMutex.release()
        return frame

    @property
    def latestPose(self):
        self._poseMutex.acquire()
        pose = self._pose
        self._poseMutex.release()
        return pose

    @property
    def latestImage(self):
        self._poseMutex.acquire()
        image = self._image
        self._poseMutex.release()
        return image


if __name__ == "__main__":
    import cv2

    world_matrix = np.array([[686.26555927, 0, 328.88594766],
                             [0, 680.31999716, 248.20539324],
                             [0, 0, 1]], dtype=np.float32)
    world_distortion = np.array([0.176468296, -0.765735942, 0.00031101025,
                                 -0.00105836974, 0.379719505], dtype=np.float32)

    aruco_detector = ArucoDetector(world_matrix, world_distortion)
    CONFIG.ARUCO_TEST = True

    corners_dict = {}

    device_list = uvc.device_list()
    pyuvcThreads = [
        # PyuvcPoseThread(device_list[0]["uid"], 34, {"Auto Focus": 0, "Absolute Focus": 14}),
        PyuvcCameraThread(device_list[0]["uid"], 34, {"Auto Focus": 0, "Absolute Focus": 13}),
        # PyuvcCameraThread(device_list[3]["uid"], 11)
    ]

    for thread in pyuvcThreads:
        thread.start()

    while True:
        for iteration, thread in enumerate(pyuvcThreads):
            #     if isinstance(thread, PyuvcPoseThread):
            #         print(thread.latestPose)
            ret, frame = thread.read()
            if ret is True:
                aruco_detection = aruco_detector.detect(frame, frame)
                if not aruco_detection:
                    cv2.imshow(f"frame_{iteration}", frame)
                    continue

                display_rotation_wcs, display_rotation_matrix, display_position_wcs, normal_wcs, world_img, corners \
                    = aruco_detection
                if corners is not None:
                    POINTS_ROW = CONFIG.CHECKERBOARD_COLUMNS - 1
                    POINTS_COL = CONFIG.CHECKERBOARD_ROWS - 1
                    SQUARE_LENGTH = 16.146
                    OBJ_POINTS = (np.array(
                        [(i // POINTS_COL, i % POINTS_COL, 0) for i in
                         range(POINTS_ROW * POINTS_COL)]) * SQUARE_LENGTH - [
                                      SQUARE_LENGTH * (POINTS_ROW - 1) / 2, SQUARE_LENGTH * (POINTS_COL - 1) / 2,
                                      0]) * [1, 1, 1]

                    # obj_points_transformed = MathHelpers.inverse_transform(OBJ_POINTS, display_position_wcs,
                    #                                                        display_rotation_matrix)

                    image_points, _ = cv2.projectPoints(
                        objectPoints=OBJ_POINTS,
                        rvec=display_rotation_wcs,
                        tvec=display_position_wcs,
                        cameraMatrix=world_matrix,
                        distCoeffs=world_distortion
                    )

                    distance_total = 0
                    min_pixel_error = ctypes.windll.user32.GetSystemMetrics(0)
                    max_pixel_error = 0

                    for ip, point in enumerate(corners):
                        dist = np.linalg.norm(point - image_points[ip])
                        distance_total += dist

                        if dist < min_pixel_error:
                            min_pixel_error = dist
                        if dist > max_pixel_error:
                            max_pixel_error = dist
                        cv2.circle(frame, (point.ravel()[0].astype(int), point.ravel()[1].astype(int)), 2, (0, 0, 0), -1)

                    for point in image_points:
                        cv2.circle(frame, (point.ravel()[0].astype(int), point.ravel()[1].astype(int)), 1, (150, 150, 150), -1)

                    camera_display_dist_mm = np.linalg.norm(display_position_wcs)

                    # Converting average pixel error to angle
                    average_dist_px = distance_total / len(corners)
                    average_dist_mm = CONFIG.PPMM * average_dist_px
                    print("Average distance in mm:", average_dist_mm)
                    angle_tan = average_dist_mm / 2 / camera_display_dist_mm
                    average_angle_error = np.rad2deg(math.atan(angle_tan) * 2)
                    print("Average angle error:", average_angle_error)

                    # Converting maximal pixel error to angle
                    max_mm_error = CONFIG.PPMM * max_pixel_error
                    max_angle_tan_error = max_mm_error / 2 / camera_display_dist_mm
                    max_angle_error = np.rad2deg(math.atan(max_angle_tan_error) * 2)
                    print("Maximal angle error:", max_angle_error)

                    # Converting minimal pixel error to angle
                    min_mm_error = CONFIG.PPMM * min_pixel_error
                    min_angle_tan_error = min_mm_error / 2 / camera_display_dist_mm
                    min_angle_error = np.rad2deg(math.atan(min_angle_tan_error) * 2)
                    print("Minimal angle error:", min_angle_error)

                    # print("CORNERS (GROUND TRUTH):", corners)
                    # print("IMAGE POINTS:", image_points)

                cv2.imshow(f"frame_{iteration}", cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR))

        waitedKey = cv2.waitKey(1) & 0xff
        if waitedKey == ord('q'):
            break
    for t in pyuvcThreads:
        t.stop()
        t.join()
