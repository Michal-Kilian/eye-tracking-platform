import cv2
import uvc


def main():

    for device in uvc.device_list():

        cap = uvc.Capture(device["uid"])

        for mode in cap.available_modes[-1:]:
            # print(f"{cap.name} running at {mode}")
            try:
                cap.frame_mode = mode
            except uvc.InitError as err:
                # print(f"{cap.name} mode selection - {err}")
                continue
            try:
                while True:
                    frame = cap.get_frame_robust()
                    cv2.imshow("frame", frame.gray)
                    cv2.waitKey(10)
                    # print("frame gray mean", frame.gray.mean())
                # print(frame.img.mean())
            except uvc.InitError as err:
                ...
                # print(f"{cap.name} getting frames - {err}")

        cap.close()

    # Uncomment the following lines to configure the Pupil 200Hz IR cameras:
    # controls_dict = dict([(c.display_name, c) for c in cap.controls])
    # controls_dict['Auto Exposure Mode'].value = 1
    # controls_dict['Gamma'].value = 200

    # cap.frame_mode = cap.avaible_modes[0]
    # for x in range(100):
    #     frame = cap.get_frame_robust()
    #     print(frame.img.mean())
    # cap = None


if __name__ == "__main__":
    # logging.basicConfig(
    #     level=logging.NOTSET,
    #     handlers=[RichHandler(level="DEBUG")],
    #     format="%(message)s",
    #     datefmt="[%X]",
    # )
    main()
