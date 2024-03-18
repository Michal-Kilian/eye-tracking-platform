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

    def check_supported(self):
        supported_devices = get_supported_devices()
        for device in supported_devices:
            if device["name"] == self.name:
                return True
        return False

    def get_matrix_coefficients(self):
        supported_devices = get_supported_devices()
        for device in supported_devices:
            if device["name"] == self.name:
                return device["matrix_coefficients"]

    def get_distortion_coefficients(self):
        supported_devices = get_supported_devices()
        for device in supported_devices:
            if device["name"] == self.name:
                return device["distortion_coefficients"]


RIGHT_EYE_DEVICE = None
LEFT_EYE_DEVICE = None
WORLD_DEVICE = None

ARUCO_TYPE = cv2.aruco.DICT_4X4_50


def get_supported_devices():
    f = open("backend/CONFIG.json")
    return json.load(f)["supported_devices"]


def get_uvc_devices():
    return uvc.device_list()


SUPPORTED_DEVICES = get_supported_devices()
