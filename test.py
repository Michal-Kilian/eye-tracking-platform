import cv2
from backend import Devices
from backend.ArucoDetector import ArucoDetector
import uvc


class MainTest:
    def __init__(self):
        super().__init__()
        self.aruco_detector = ArucoDetector()
        self.cap = uvc.Capture(Devices.WORLD_DEVICE.uid)
        self.cap.frame_mode = self.cap.available_modes[34]
        self.controls_dict = dict([(c.display_name, c) for c in self.cap.controls])
        self.controls_dict['Auto Focus'].value = 0
        self.controls_dict['Absolute Focus'].value = 13

    def start(self):
        while True:
            frame = self.cap.get_frame_robust()
            self.aruco_detector.detect(frame)
            cv2.imshow("Detected Markers", frame.bgr)
            cv2.waitKey(10)

    def stop(self):
        cv2.destroyAllWindows()

    def get_current_abs_focus(self):
        return self.cap.controls[3].value


if __name__ == "__main__":
    maintest = MainTest()
    maintest.start()
