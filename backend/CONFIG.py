import json
from typing import TextIO
import numpy as np
from Helpers import MathHelpers


def get_supported_devices() -> list:
    f: TextIO = open("backend/CONFIG.json")
    return json.load(f)["supported_devices"]


def get_2d_parameters() -> dict:
    f: TextIO = open("backend/CONFIG.json")
    return json.load(f)["detector_2D_parameters"]


def get_3d_parameters() -> dict:
    f: TextIO = open("backend/CONFIG.json")
    return json.load(f)["detector_3D_parameters"]


def get_2d_default_parameters() -> dict:
    f: TextIO = open("backend/CONFIG.json")
    return json.load(f)["detector_2D_default_parameters"]


def get_3d_default_parameters() -> dict:
    f = open("backend/CONFIG.json")
    return json.load(f)["detector_3D_default_parameters"]


def update_config(section: str) -> None:
    with open("backend/CONFIG.json", "r") as file:
        config_dict = json.load(file)

    if section == "parameters":
        config_dict["detector_2D_parameters"] = PARAMETERS_2D
        config_dict["detector_3D_parameters"] = PARAMETERS_3D

        with open("backend/CONFIG.json", "w") as file:
            json.dump(config_dict, file, indent=4)


def reset_config(section: str) -> None:
    with open("backend/CONFIG.json", "r") as file:
        config_dict = json.load(file)

    if section == "parameters":
        config_dict["detector_2D_parameters"] = get_2d_default_parameters()
        config_dict["detector_3D_parameters"] = get_3d_default_parameters()

        with open("backend/CONFIG.json", "w") as file:
            json.dump(config_dict, file, indent=4)


def get_focal_length():
    f = open("backend/CONFIG.json")
    return json.load(f)["offline_focal_length"]


def get_resolution():
    f = open("backend/CONFIG.json")
    return json.load(f)["offline_resolution"]


def get_elevation():
    f = open("backend/CONFIG.json")
    return json.load(f)["elevation"]


def get_azimuth():
    f = open("backend/CONFIG.json")
    return json.load(f)["azimuth"]


def get_scale_factor():
    f = open("backend/CONFIG.json")
    return json.load(f)["scale_factor"]


def get_camera_position(camera_type: str):
    if TEST and camera_type == "right":
        return np.array([-30, -30, 0])
    elif TEST and camera_type == "left":
        return np.array([30, -30, 0])
    ...


def get_camera_rotation_matrix(camera_type: str):
    if TEST:
        return
    ...


SUPPORTED_DEVICES = get_supported_devices()
PARAMETERS_2D = get_2d_parameters()
PARAMETERS_3D = get_3d_parameters()
PICTURE_SELECTED = None
MODE_SELECTED = None

OFFLINE_MODE_DIRECTORY = "images"
OFFLINE_MODE_MAX_ID = 120
OFFLINE_MODE_MIN_ID = 0
OFFLINE_FOCAL_LENGTH = get_focal_length()
OFFLINE_RESOLUTION = get_resolution()
OFFLINE_CAMERA_POSITION = np.array([20, -50, -10])
OFFLINE_CAMERA_ROTATION_MATRIX = np.array([
    [0.884918212890625, -0.105633445084095, -0.4536091983318329],
    [0.4657464325428009, 0.20070354640483856, 0.8618574738502502],
    [0.0, -0.973940372467041, 0.22680459916591644]
])
OFFLINE_DISPLAY_POSITION = np.array([0, -500, 0])
OFFLINE_DISPLAY_ROTATION = np.array([0, 0, 180])
OFFLINE_DISPLAY_ROTATION_MATRIX = MathHelpers.euler_to_rot(OFFLINE_DISPLAY_ROTATION)
OFFLINE_DISPLAY_NORMAL_LOCAL = np.array([0, -1, 0])
OFFLINE_DISPLAY_NORMAL_WORLD = MathHelpers.normalize(MathHelpers.rotate(OFFLINE_DISPLAY_NORMAL_LOCAL,
                                                                        OFFLINE_DISPLAY_ROTATION_MATRIX))
OFFLINE_CAMERA_DIRS_WORLD = (
            MathHelpers.rotate(np.array((1, 0, 0)), OFFLINE_CAMERA_ROTATION_MATRIX),
            MathHelpers.rotate(np.array((0, 1, 0)), OFFLINE_CAMERA_ROTATION_MATRIX),
            MathHelpers.rotate(np.array((0, 0, 1)), OFFLINE_CAMERA_ROTATION_MATRIX)
        )

ELEVATION = get_elevation()
AZIMUTH = get_azimuth()
SCALE_FACTOR = get_scale_factor()

RIGHT_EYE_CAMERA_POSITION = np.array([-30, -30, 0])
# RIGHT_EYE_CAMERA_POSITION = get_camera_position("right")
RIGHT_EYE_CAMERA_ROTATION_MATRIX = MathHelpers.euler_to_rot((0, -180, 0))
# RIGHT_EYE_CAMERA_ROTATION_MATRIX = get_camera_rotation_matrix("right")

LEFT_EYE_CAMERA_POSITION = np.array([30, -30, 0])
# LEFT_EYE_CAMERA_POSITION = get_camera_position("left")
LEFT_EYE_CAMERA_ROTATION_MATRIX = MathHelpers.euler_to_rot((0, -180, 0))
# LEFT_EYE_CAMERA_ROTATION_MATRIX = get_camera_rotation_matrix("left")

DISPLAY_WIDTH = 310
DISPLAY_HEIGHT = 174

OFFLINE_DISPLAY_WIDTH = 250
OFFLINE_DISPLAY_HEIGHT = 250

TEST = False
