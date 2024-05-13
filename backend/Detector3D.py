import numpy as np
from pye3d.detector_3d import Detector3D as Det3D, CameraModel, DetectorMode
from backend import Devices
from Helpers import MathHelpers
from backend import CONFIG
from backend import RECORDS


class Detector3D:
    def __init__(self, camera_type: str = None):
        if CONFIG.MODE_SELECTED == RECORDS.RecordType.REAL_TIME:
            if camera_type == "right":
                self.camera = Devices.RIGHT_EYE_DEVICE
                self.camera_model: CameraModel = CameraModel(focal_length=Devices.RIGHT_EYE_DEVICE.focal_length,
                                                             resolution=Devices.RIGHT_EYE_DEVICE.resolution)
            elif camera_type == "left":
                self.camera = Devices.LEFT_EYE_DEVICE
                self.camera_model: CameraModel = CameraModel(focal_length=Devices.LEFT_EYE_DEVICE.focal_length,
                                                             resolution=Devices.LEFT_EYE_DEVICE.resolution)
            else:
                self.camera = Devices.WORLD_DEVICE
                self.camera_model: CameraModel = CameraModel(focal_length=Devices.WORLD_DEVICE.focal_length,
                                                             resolution=Devices.WORLD_DEVICE.resolution)
            self.apply_refraction_correction: bool = True
        else:
            self.camera_model: CameraModel = CameraModel(focal_length=CONFIG.OFFLINE_FOCAL_LENGTH,
                                                         resolution=CONFIG.OFFLINE_RESOLUTION)
            self.apply_refraction_correction: bool = False

        self.detector: Det3D = Det3D(camera=self.camera_model)
        self.detector.update_properties(CONFIG.PARAMETERS_3D)

    def detect(self, result_2d, frame_gray, display_normal_wcs, display_position_wcs, display_rotation_matrix):

        result = self.detector.update_and_detect(result_2d, frame_gray,
                                                 apply_refraction_correction=self.apply_refraction_correction)

        eye_position_wcs = MathHelpers.transform(
            np.array(result["sphere"]["center"]),
            CONFIG.LEFT_EYE_CAMERA_POSITION, CONFIG.LEFT_EYE_CAMERA_ROTATION_MATRIX)

        gaze_ray_wcs = MathHelpers.normalize(MathHelpers.rotate(result["circle_3d"]["normal"],
                                                                CONFIG.LEFT_EYE_CAMERA_ROTATION_MATRIX))

        intersection_time = MathHelpers.intersect_plane(display_normal_wcs, display_position_wcs,
                                                        eye_position_wcs, gaze_ray_wcs)

        if intersection_time < 0:
            return None, None, None, None, None

        plane_intersection_wcs = MathHelpers.get_point([eye_position_wcs, gaze_ray_wcs], intersection_time)

        plane_intersection_local = MathHelpers.inverse_transform(plane_intersection_wcs, display_position_wcs,
                                                                 display_rotation_matrix)

        uv_coords = MathHelpers.convert_to_uv(plane_intersection_local, CONFIG.DISPLAY_WIDTH, CONFIG.DISPLAY_HEIGHT)

        return uv_coords, eye_position_wcs, gaze_ray_wcs, plane_intersection_wcs, plane_intersection_local

    def detect_offline(self, result_2d, frame_gray):
        result = self.detector.update_and_detect(result_2d, frame_gray,
                                                 apply_refraction_correction=self.apply_refraction_correction)

        eye_pos_world = MathHelpers.transform(np.array(result["sphere"]["center"]),
                                              CONFIG.OFFLINE_CAMERA_POSITION, CONFIG.OFFLINE_CAMERA_ROTATION_MATRIX)
        gaze_ray = MathHelpers.normalize(MathHelpers.rotate(result["circle_3d"]["normal"],
                                                            CONFIG.OFFLINE_CAMERA_ROTATION_MATRIX))

        intersection_time = MathHelpers.intersect_plane(CONFIG.OFFLINE_DISPLAY_NORMAL_WORLD,
                                                        CONFIG.OFFLINE_DISPLAY_POSITION,
                                                        eye_pos_world, gaze_ray)

        plane_intersection = np.array([0, 0, 0])
        if intersection_time > 0.0:
            plane_intersection = MathHelpers.get_point([eye_pos_world, gaze_ray], intersection_time)

        return plane_intersection, eye_pos_world, gaze_ray
