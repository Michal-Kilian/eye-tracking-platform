import uvc
import cv2
import numpy as np
from backend import CONFIG


class Device:
    def __init__(self, name):
        self.name = name
        self.uid = self.get_uid()
        self.supported = self.check_supported()
        self.matrix_coefficients = self.get_matrix_coefficients()
        self.distortion_coefficients = self.get_distortion_coefficients()
        self.absolute_focus = self.get_absolute_focus()
        self.focal_length = self.get_focal_length()
        self.resolution = self.get_resolution()
        self.auto_focus = self.get_auto_focus()

    def get_uid(self):
        for device in get_uvc_devices():
            if device["name"] == self.name:
                return device["uid"]
        return None

    def check_supported(self):
        for device in CONFIG.SUPPORTED_DEVICES:
            if device["name"] == self.name:
                return True
        return False

    def get_matrix_coefficients(self):
        config_matrix = []
        for device in CONFIG.SUPPORTED_DEVICES:
            if device["name"] == self.name:
                config_matrix = device["matrix_coefficients"]

        if config_matrix:
            return np.array((
                (config_matrix[0][0], config_matrix[0][1], config_matrix[0][2]),
                (config_matrix[1][0], config_matrix[1][1], config_matrix[1][2]),
                (config_matrix[2][0], config_matrix[2][1], config_matrix[2][2])
            ))
        else:
            return None

    def get_distortion_coefficients(self):
        config_dist = []
        for device in CONFIG.SUPPORTED_DEVICES:
            if device["name"] == self.name:
                config_dist = device["distortion_coefficients"]

        if config_dist:
            return np.array((
                config_dist[0], config_dist[1], config_dist[2], config_dist[3], config_dist[4]
            ))
        else:
            return None

    def get_absolute_focus(self):
        for device in CONFIG.SUPPORTED_DEVICES:
            if device["name"] == self.name:
                return device["absolute_focus"]
        return None

    def get_focal_length(self):
        config_matrix = []
        for device in CONFIG.SUPPORTED_DEVICES:
            if device["name"] == self.name:
                config_matrix = device["matrix_coefficients"]

        if config_matrix:
            return (config_matrix[0][0] + config_matrix[1][1]) / 2
        else:
            return None

    def get_resolution(self):
        cap = uvc.Capture(self.uid)
        return [640, 480]

    def get_auto_focus(self):
        for device in CONFIG.SUPPORTED_DEVICES:
            if device["name"] == self.name:
                return device["auto_focus"]
        return None


RIGHT_EYE_DEVICE = None
LEFT_EYE_DEVICE = None
WORLD_DEVICE = None

ARUCO_TYPE = cv2.aruco.DICT_4X4_50


def get_uvc_devices():
    return uvc.device_list()


def is_device_online(device_name):
    for device in uvc.device_list():
        if device["name"] == device_name:
            return True
    return False
