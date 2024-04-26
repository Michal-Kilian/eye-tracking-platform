import json
from typing import TextIO


def get_supported_devices():
    f: TextIO = open("backend/CONFIG.json")
    return json.load(f)["supported_devices"]


def get_2d_default_parameters() -> dict:
    f: TextIO = open("backend/CONFIG.json")
    return json.load(f)["detector_2D_default_parameters"]


def get_3d_default_parameters() -> dict:
    f = open("backend/CONFIG.json")
    return json.load(f)["detector_3D_default_parameters"]


SUPPORTED_DEVICES = get_supported_devices()
PARAMETERS_2D = get_2d_default_parameters()
PARAMETERS_3D = get_3d_default_parameters()
