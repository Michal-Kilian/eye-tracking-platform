import uvc

RIGHT_EYE_DEVICE = None
LEFT_EYE_DEVICE = None
MIDDLE_DEVICE = None


def find_device_from_name(device_name):

    for device in uvc.device_list():
        if device["name"] == device_name:
            return device

    return None
