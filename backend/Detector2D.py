import uvc
import cv2
from pupil_detectors import Detector2D as Det2D
from backend import Devices, CONFIG


class Detector2D:
    def __init__(self):
        self.detector = Det2D(CONFIG.PARAMETERS_2D)
        self.cap = uvc.Capture(Devices.LEFT_EYE_DEVICE.uid)
        self.cap.frame_mode = self.cap.available_modes[34]
        self.controls_dict = dict([(c.display_name, c) for c in self.cap.controls])
        self.controls_dict['Auto Focus'].value = 0
        self.controls_dict['Absolute Focus'].value = 40
        self.frame_generator = frame_generator(120, "./" + CONFIG.OFFLINE_MODE_DIRECTORY + "/example_{0}.png")

    def detect(self):
        if CONFIG.MODE_SELECTED == "real-time":
            frame = self.cap.get_frame_robust()
            frame_bgr = frame.bgr
            frame_gray = frame.gray
        else:
            frame_bgr = next(self.frame_generator)
            frame_gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)

        result = self.detector.detect(frame_gray, frame_bgr)

        # draw the ellipse outline onto the input image
        # note that cv2.ellipse() cannot deal with float values
        # also it expects the axes to be semi-axes (half the size)
        # cv2.ellipse(
        #     frame,
        #     tuple(int(v) for v in result["ellipse"]["center"]),
        #     tuple(int(v / 2) for v in result["ellipse"]["axes"]),
        #     result["ellipse"]["angle"],
        #     0,
        #     360,
        #     (0, 255, 0),
        # )
        cv2.imshow("Image", frame_bgr)
        cv2.waitKey(10)

        return frame_bgr

    def stop(self):
        cv2.destroyAllWindows()


def frame_generator(max_id: int, path_format: str):
    num = 0
    while True:
        yield cv2.imread(path_format.format(num))
        num = (num + 1) % (max_id + 1)
