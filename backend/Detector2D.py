import time

import numpy as np
import uvc
import cv2
from pupil_detectors import Detector2D as Det2D
from backend import Devices, CONFIG
from backend import RECORDS


class Detector2D:
    def __init__(self):
        self.detector = Det2D(CONFIG.PARAMETERS_2D)

    def detect(self, frame_gray, frame_bgr=None):
        if frame_bgr is None:
            result = self.detector.detect(frame_gray)
            result["timestamp"] = time.time()
            print(result)
            return result, frame_gray
        else:
            frame_bgr_1 = np.copy(frame_bgr)
            frame_bgr_2 = np.copy(frame_bgr)
            result = self.detector.detect(frame_gray, frame_bgr_1)
            cv2.ellipse(
                frame_bgr_2,
                tuple(int(v) for v in result["ellipse"]["center"]),
                tuple(int(v / 2) for v in result["ellipse"]["axes"]),
                result["ellipse"]["angle"],
                0,
                360,
                (0, 255, 0),
            )
            result["timestamp"] = time.time()
            return result, frame_gray, frame_bgr_1, frame_bgr_2
