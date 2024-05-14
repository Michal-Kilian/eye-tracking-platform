import cv2
import uvc


class DevicePreview:
    def __init__(self, device):
        self.device = device
        self.cap = uvc.Capture(self.device.uid)
        self.cap.frame_mode = self.cap.available_modes[self.device.mode_index]
        self.running = False

    def start(self):
        self.running = True
        while self.running:
            frame = self.cap.get_frame_robust()
            cv2.imshow(self.device.name + " Preview", frame.bgr)
            cv2.waitKey(1)

    def stop(self):
        self.running = False
        cv2.destroyAllWindows()
