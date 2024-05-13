import time
import uvc
import cv2
from pupil_detectors import Detector2D as Det2D
from backend import Devices, CONFIG
from backend import RECORDS


class Detector2D:
    def __init__(self, camera: Devices.Device = None):
        self.detector = Det2D(CONFIG.PARAMETERS_2D)

        if CONFIG.MODE_SELECTED == RECORDS.RecordType.REAL_TIME and camera is not None:
            self.cap = uvc.Capture(camera)
            self.controls_dict = dict([(c.display_name, c) for c in self.cap.controls])
            self.controls_dict['Auto Focus'].value = camera.auto_focus
            self.controls_dict['Absolute Focus'].value = camera.absolute_focus

    def detect(self, frame_gray, frame_bgr):
        result = self.detector.detect(frame_gray, frame_bgr)
        result["timestamp"] = time.time()

        return result, frame_gray, frame_bgr
