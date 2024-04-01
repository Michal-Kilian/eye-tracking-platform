import uvc
import cv2
import json
import numpy as np


class Device:
    def __init__(self, name):
        self.name = name
        self.uid = self.get_uid()
        self.supported = self.check_supported()
        self.matrix_coefficients = self.get_matrix_coefficients()
        self.distortion_coefficients = self.get_distortion_coefficients()

    def get_uid(self):
        device_list = get_uvc_devices()
        for device in device_list:
            if device["name"] == self.name:
                return device["uid"]
        return False

    def check_supported(self):
        supported_devices = get_supported_devices()
        for device in supported_devices:
            if device["name"] == self.name:
                return True
        return False

    def get_matrix_coefficients(self):
        supported_devices = get_supported_devices()
        config_matrix = []

        for device in supported_devices:
            if device["name"] == self.name:
                config_matrix = device["matrix_coefficients"]

        return np.array((
            (config_matrix[0][0], config_matrix[0][1], config_matrix[0][2]),
            (config_matrix[1][0], config_matrix[1][1], config_matrix[1][2]),
            (config_matrix[2][0], config_matrix[2][1], config_matrix[2][2])
        ))

    def get_distortion_coefficients(self):
        supported_devices = get_supported_devices()
        config_dist = []

        for device in supported_devices:
            if device["name"] == self.name:
                config_dist = device["distortion_coefficients"]

        return np.array((
            config_dist[0], config_dist[1], config_dist[2], config_dist[3], config_dist[4]
        ))


RIGHT_EYE_DEVICE = None
LEFT_EYE_DEVICE = None
WORLD_DEVICE = None

ARUCO_TYPE = cv2.aruco.DICT_4X4_50


def get_supported_devices():
    f = open("backend/CONFIG.json")
    return json.load(f)["supported_devices"]


def get_uvc_devices():
    return uvc.device_list()


def is_device_online(device_name):
    for device in uvc.device_list():
        if device["name"] == device_name:
            return True
    return False


SUPPORTED_DEVICES = get_supported_devices()
