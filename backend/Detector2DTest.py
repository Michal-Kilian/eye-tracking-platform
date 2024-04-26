import uvc
import cv2
from pupil_detectors import Detector2D
from backend import Devices


class Detector2DTest:
    def __init__(self):
        self.detector = Detector2D()
        self.cap = uvc.Capture(Devices.LEFT_EYE_DEVICE.uid)
        self.cap.frame_mode = self.cap.available_modes[34]
        self.controls_dict = dict([(c.display_name, c) for c in self.cap.controls])
        self.controls_dict['Auto Focus'].value = 0
        self.controls_dict['Absolute Focus'].value = 13
        self.running = None

    def start(self):
        self.running = True
        while self.running:
            frame = self.cap.get_frame_robust()

            result = self.detector.detect(frame.gray)
            ellipse = result["ellipse"]

            # draw the ellipse outline onto the input image
            # note that cv2.ellipse() cannot deal with float values
            # also it expects the axes to be semi-axes (half the size)
            cv2.ellipse(
                frame.bgr,
                tuple(int(v) for v in ellipse["center"]),
                tuple(int(v / 2) for v in ellipse["axes"]),
                ellipse["angle"],
                0, 360,  # start/end angle for drawing
                (0, 0, 255)  # color (BGR): red
            )
            cv2.imshow("Image", frame.bgr)
            cv2.waitKey(0)

    def stop(self):
        self.running = False
        cv2.destroyAllWindows()


if __name__ == '__main__':
    ...
