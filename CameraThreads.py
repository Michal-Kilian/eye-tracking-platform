import abc
import json
import threading
import uvc
import numpy as np
from Helpers import MathHelpers
from backend import CONFIG
from backend.Detector2D import Detector2D
from backend.Detector3D import Detector3D


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
        while (True):
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

    def __init__(self, uid, modeIndex, controls={}):
        super().__init__()
        self._uid = uid
        self._cap = None
        self._modeIndex = modeIndex
        self._controls = controls
        self._allControls = None
        self._resolution = None
        return

    def _tinit(self):
        self._cap = uvc.Capture(self._uid)
        self._cap.frame_mode = self._cap.available_modes[self._modeIndex]
        self._allControls = {c.display_name: c for c in self._cap.controls}

        for k, v in self._controls.items():
            self._allControls[k].value = v
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
            frame = cv2.resize(self._cap.get_frame().gray, (0,0), fx=1, fy=1)
        except Exception as e:
            print("Could not get frame, reset")
            self._tinit()
        return frame


class PyuvcPoseThread(PyuvcCameraThread):

    def __init__(self, uid, modeIndex, controls={}, markerLength=34.8, cameraMatrix=np.eye(3),
                 distortionCoeffs=np.zeros(8)):
        super().__init__(uid, modeIndex, controls)
        self._arucoDetector = None
        self._markerLength = markerLength
        self._cm = cameraMatrix
        self._dcs = distortionCoeffs
        self._poseMutex = threading.Lock()
        self._pose = None, None
        return

    def _tinit(self):
        super()._tinit()
        detectorDictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        detectorParameters = cv2.aruco.DetectorParameters()
        self._arucoDetector = cv2.aruco.ArucoDetector(detectorDictionary, detectorParameters)
        return

    def _getPose(self, image):
        corners, ids, _ = self._arucoDetector.detectMarkers(image)
        if len(corners) > 3:
            totalTvec = np.zeros(3)
            tvecDict = {}

            for i in range(len(ids)):
                mid = ids[i][0]
                if mid <= 3:
                    rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(
                        corners[i],
                        self._markerLength,
                        self._cm,
                        self._dcs
                    )
                    totalTvec += tvec.ravel()
                    tvecDict[mid] = tvec.ravel()

            if len(tvecDict) != 4:
                return None, None

            avg13 = (tvecDict[1] + tvecDict[3]) * 0.5
            avg02 = (tvecDict[0] + tvecDict[2]) * 0.5
            xVec = avg13 - avg02

            avg01 = (tvecDict[0] + tvecDict[1]) * 0.5
            avg23 = (tvecDict[2] + tvecDict[3]) * 0.5
            yVec = avg01 - avg23

            nxVec = MathHelpers.normalize(xVec).ravel()
            nyVec = MathHelpers.normalize(yVec).ravel()
            nzVec = MathHelpers.normalize(MathHelpers.cross_product(nxVec, nyVec)).ravel()

            rotMat = np.array([
                [nxVec[0], nyVec[0], nzVec[0]],
                [nxVec[1], nyVec[1], nzVec[1]],
                [nxVec[2], nyVec[2], nzVec[2]]]
            )

            return rotMat, totalTvec / len(totalTvec)

        return None, None

    def _readImage(self):
        frame = super()._readImage()
        if frame is not None:
            pose = self._getPose(frame)
            if pose[0] is not None:
                self._poseMutex.acquire()
                self._pose = pose
                self._poseMutex.release()
        return frame

    @property
    def latestPose(self):
        self._poseMutex.acquire()
        pose = self._pose
        self._poseMutex.release()
        return pose


def detect_gaze(frame_gray, display_position_wcs, display_rotation_matrix, detector_3d, eye):
    frame_bgr_1, frame_bgr_2 = None, None
    if eye == "left":
        frame_bgr = cv2.cvtColor(frame_gray, cv2.COLOR_GRAY2BGR)
        result_2d, frame_gray, frame_bgr_1, frame_bgr_2 = detector_2d.detect(frame_gray, frame_bgr)
    else:
        result_2d, frame_gray = detector_2d.detect(frame_gray)

    display_normal_wcs = MathHelpers.normalize(MathHelpers.rotate(np.array([0, 0, 1]), display_rotation_matrix))

    result_3d = None
    frame = None
    if result_2d["confidence"] > 0.75:
        result_3d, eye_pos_world, gaze_ray, plane_intersection_wcs, \
            plane_intersection_local, frame = (
                detector_3d.detect(
                    result_2d, frame_gray,
                    display_normal_wcs,
                    display_position_wcs,
                    display_rotation_matrix
                ))
    if eye == "left":
        return result_3d, frame, frame_bgr_2
    else:
        return result_3d


def get_device_config(index):
    f = open("backend/CONFIG.json")
    return json.load(f)["supported_devices"][index]


def get_focal_length(device_config):
    return (device_config["matrix_coefficients"][0][0] + device_config["matrix_coefficients"][1][1]) / 2


def get_resolution(uid, mode_index):
    cap = uvc.Capture(uid)
    return [cap.available_modes[mode_index].width,
            cap.available_modes[mode_index].height]


def get_final_uv_coords(right_result_3d, left_result_3d):
    if not right_result_3d:
        final_uv_coords = left_result_3d
    elif not left_result_3d:
        final_uv_coords = right_result_3d
    else:
        final_uv_coords = ((right_result_3d[0] + left_result_3d[0]) / 2,
                           (right_result_3d[1] + left_result_3d[1]) / 2)
    return final_uv_coords


if __name__ == "__main__":
    import cv2

    world_device_config = get_device_config(0)

    deviceList = uvc.device_list()
    pyuvcThreads = [
        PyuvcPoseThread(deviceList[0]["uid"], -1, {"Auto Focus": 1, "Absolute Focus": 14},
                        cameraMatrix=np.array(world_device_config["matrix_coefficients"]),
                        distortionCoeffs=np.array(world_device_config["distortion_coefficients"])),
        # PyuvcCameraThread(deviceList[1]["uid"], 11, {"Absolute Exposure Time": 20, "Gamma": 120}),
        PyuvcCameraThread(deviceList[1]["uid"], 11, {"Absolute Exposure Time": 20, "Gamma": 120})
    ]
    # "Auto Exposure Mode": 0,
    # right_device_config = get_device_config(1)
    left_device_config = get_device_config(2)

    print(world_device_config)
    # print(right_device_config)
    print(left_device_config)

    detector_2d = Detector2D()
    # detector_3d_right = Detector3D(np.array(right_device_config["position"]), np.array(right_device_config["rotation_matrix"]),
    #                                get_focal_length(right_device_config),
    #                                get_resolution(deviceList[1]["uid"], right_device_config["mode_index"]))
    detector_3d_left = Detector3D(np.array(left_device_config["position"]), np.array(left_device_config["rotation_matrix"]),
                                  get_focal_length(left_device_config),
                                  get_resolution(deviceList[1]["uid"], left_device_config["mode_index"]))

    # for t in pyuvcThreads:
    #     t.start()
    pyuvcThreads[0].start()
    pyuvcThreads[1].start()

    while True:
        pose = pyuvcThreads[0].latestPose
        print("pose:", pose)
        world_ret, world_frame = pyuvcThreads[0].read()

        if pose[0] is not None:
            right_uv_coords, left_uv_coords = None, None
            frame_1, frame_2 = None, None

            # right_ret, right_frame = pyuvcThreads[1].read()
            # if right_ret is True:
            #     right_uv_coords, frame_1, frame_2 = detect_gaze(right_frame, pose[1], pose[0], detector_3d_right, "right")

            left_ret, left_frame = pyuvcThreads[1].read()
            if left_ret is True:
                left_uv_coords, frame_1, frame_2 = detect_gaze(left_frame, pose[1], pose[0], detector_3d_left, "left")

            if world_ret is True:
                print(world_frame.shape)
                test_frame = np.copy(world_frame)
                test_frame = (test_frame * 0.1).astype(np.uint8)
                final_uv = get_final_uv_coords(right_uv_coords, left_uv_coords)
                if final_uv is not None:
                    image_coords = np.array([final_uv[0] * world_frame.shape[1], final_uv[1] * world_frame.shape[0]], dtype=int)
                    cv2.circle(test_frame, image_coords, 10, (255, 255, 255), 2)
                cv2.imshow("frame", cv2.resize(test_frame, (0,0), fx=0.5, fy=0.5))
                cv2.moveWindow("frame", 0, 0)

                if frame_1 is not None:
                    cv2.imshow("frame_1", frame_1)
                    cv2.imshow("frame_2", frame_2)
                    cv2.moveWindow("frame_1", 200, 200)
                    cv2.moveWindow("frame_2", 400, 400)
                    ...
            else:
                pass
                # print("No world image")

        waitedKey = cv2.waitKey(1) & 0xff
        if waitedKey == ord('q'):
            break
    for t in pyuvcThreads:
        t.stop()
        t.join()
