import cv2

from backend import Devices
from backend.ArucoDetector import ArucoDetector
import uvc
import backend.Devices


def main():
    print("world device in test.py:", Devices.WORLD_DEVICE.name)
    aruco_detector = ArucoDetector()
    cap = uvc.Capture(Devices.WORLD_DEVICE.uid)
    cap.frame_mode = cap.available_modes[34]
    print(cap.frame_mode)

    while True:
        frame = cap.get_frame_robust()
        aruco_detector.detect(frame)
        cv2.imshow("Detected Markers", frame.bgr)
        cv2.waitKey(10)


if __name__ == "__main__":
    main()
