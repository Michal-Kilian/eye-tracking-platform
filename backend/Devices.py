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
        self.extrinsics_affine_matrix = self.get_extrinsics_affine_matrix()
        self.position = self.get_position()
        self.rotation_matrix = self.get_rotation_matrix()
        self.type = self.get_type()

    def get_uid(self):
        for device in get_uvc_devices():
            if device["name"] == self.name:
                if "uid" in device.keys():
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
                if "matrix_coefficients" in device.keys():
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
                if "distortion_coefficients" in device.keys():
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
                if "absolute_focus" in device.keys():
                    return device["absolute_focus"]
        return None

    def get_focal_length(self):
        config_matrix = []
        for device in CONFIG.SUPPORTED_DEVICES:
            if device["name"] == self.name:
                if "matrix_coefficients" in device.keys():
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
                if "auto_focus" in device.keys():
                    return device["auto_focus"]
        return None

    def get_extrinsics_affine_matrix(self):
        for device in CONFIG.SUPPORTED_DEVICES:
            if device["name"] == self.name:
                if "extrinsics_affine_matrix" in device.keys():
                    return device["extrinsics_affine_matrix"]
        return None

    def get_position(self):
        if self.extrinsics_affine_matrix is not None:
            return np.array([
                self.extrinsics_affine_matrix[0][3],
                self.extrinsics_affine_matrix[1][3],
                self.extrinsics_affine_matrix[2][3]
            ])
        return np.array([0, 0, 0])

    def get_rotation_matrix(self):
        if self.extrinsics_affine_matrix is not None:
            return np.array([
                [
                    self.extrinsics_affine_matrix[0][0],
                    self.extrinsics_affine_matrix[0][1],
                    self.extrinsics_affine_matrix[0][2]
                ],
                [
                    self.extrinsics_affine_matrix[1][0],
                    self.extrinsics_affine_matrix[1][1],
                    self.extrinsics_affine_matrix[1][2]
                ],
                [
                    self.extrinsics_affine_matrix[2][0],
                    self.extrinsics_affine_matrix[2][1],
                    self.extrinsics_affine_matrix[2][2]
                ]
            ])
        return None

    def get_type(self):
        for device in CONFIG.SUPPORTED_DEVICES:
            if device["name"] == self.name:
                if "type" in device.keys():
                    return device["type"]
        return None

    def print_self(self):
        print("---------DEVICE---------")
        print("Name:", self.name)
        print("UID:", self.uid)
        print("Supported:", self.supported)
        print("Matrix coefficients:", self.matrix_coefficients)
        print("Distortion coefficients:", self.distortion_coefficients)
        print("Absolute focus:", self.absolute_focus)
        print("Focal length:", self.focal_length)
        print("Resolution:", self.resolution)
        print("Auto focus:", self.auto_focus)
        print("Extrinsics affine matrix:", self.extrinsics_affine_matrix)
        print("Position:", self.position)
        print("Rotation matrix:", self.rotation_matrix)
        print("Type:", self.type)
        print("------------------------")


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
