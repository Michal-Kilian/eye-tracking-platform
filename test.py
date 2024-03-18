import cv2

from backend.ArucoDetector import ArucoDetector
import uvc


def main():
    aruco_detector = ArucoDetector()

    device = uvc.device_list()[0]
    cap = uvc.Capture(device["uid"])

    cap.frame_mode = cap.available_modes[-10]

    while True:
        frame = cap.get_frame_robust()
        aruco_detector.detect(frame)
        cv2.imshow("Detected Markers", frame.bgr)
        cv2.waitKey(10)


if __name__ == "__main__":
    main()
