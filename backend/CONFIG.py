import json
from typing import TextIO


def get_supported_devices():
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


SUPPORTED_DEVICES = get_supported_devices()
PARAMETERS_2D = get_2d_parameters()
PARAMETERS_3D = get_3d_parameters()
PICTURE_SELECTED = None
MODE_SELECTED = None
OFFLINE_MODE_DIRECTORY = "images"
