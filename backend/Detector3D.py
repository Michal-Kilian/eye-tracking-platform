import cv2
import numpy as np
from pye3d.detector_3d import Detector3D as Det3D, CameraModel, DetectorMode
from backend import Devices
from Helpers import MathHelpers
from backend import CONFIG
from backend import RECORDS


class Detector3D:
    def __init__(self, position=None, rotation_matrix=None, focal_length=None, resolution=None):
        self.device_position = position
        self.device_rotation_matrix = rotation_matrix
        self.device_focal_length = focal_length
        self.device_resolution = resolution

        self.camera_model: CameraModel = CameraModel(focal_length=self.device_focal_length,
                                                     resolution=self.device_resolution)
        if CONFIG.MODE_SELECTED == RECORDS.RecordType.OFFLINE:
            self.camera_model: CameraModel = CameraModel(focal_length=CONFIG.OFFLINE_FOCAL_LENGTH,
                                                         resolution=CONFIG.OFFLINE_RESOLUTION)
        """
        if CONFIG.MODE_SELECTED == RECORDS.RecordType.REAL_TIME:
            self.camera_model: CameraModel = CameraModel(focal_length=self.device_focal_length,
                                                         resolution=self.device_resolution)
            self.apply_refraction_correction: bool = True
        else:
            self.camera_model: CameraModel = CameraModel(focal_length=CONFIG.OFFLINE_FOCAL_LENGTH,
                                                         resolution=CONFIG.OFFLINE_RESOLUTION)
            self.apply_refraction_correction: bool = False
        """
        self.detector: Det3D = Det3D(camera=self.camera_model)
        self.detector.update_properties(CONFIG.PARAMETERS_3D)

    def detect(self, result_2d, frame_gray, display_normal_wcs, display_position_wcs, display_rotation_matrix):

        result = self.detector.update_and_detect(result_2d, frame_gray,
                                                 apply_refraction_correction=True)

        ellipse = result['projected_sphere']
        if ellipse["axes"][0] > 0 and ellipse["axes"][1] > 0:
            frame_gray = cv2.ellipse(frame_gray, [int(e) for e in ellipse['center']],
                                     [int(e / 2) for e in ellipse['axes']],
                                     ellipse['angle'], 0, 360, (255, 0, 0), 2)

        print("1", result["sphere"]["center"])

        print(self.device_position)
        eye_position_wcs = MathHelpers.transform(
            np.array(result["sphere"]["center"]),
            self.device_position, self.device_rotation_matrix
        )

        print("2", eye_position_wcs)

        gaze_ray_wcs = MathHelpers.normalize(
            MathHelpers.rotate(
                MathHelpers.normalize(result["circle_3d"]["normal"]),
                self.device_rotation_matrix
            )
        )

        print("3", gaze_ray_wcs)

        print(display_position_wcs)
        intersection_time = MathHelpers.intersect_plane(display_normal_wcs, display_position_wcs,
                                                        eye_position_wcs, gaze_ray_wcs)
        print("it:", intersection_time)

        if intersection_time < 0:
            print("no intersection")
            return None, None, None, None, None, None

        plane_intersection_wcs = MathHelpers.get_point([eye_position_wcs, gaze_ray_wcs], intersection_time)

        print("plane intersection:", plane_intersection_wcs)

        plane_intersection_local = MathHelpers.inverse_transform(plane_intersection_wcs, display_position_wcs,
                                                                 display_rotation_matrix)

        uv_coords = MathHelpers.convert_to_uv(plane_intersection_local, CONFIG.DISPLAY_WIDTH, CONFIG.DISPLAY_HEIGHT)

        if uv_coords is None:
            print("no uv_coords")

        return uv_coords, eye_position_wcs, gaze_ray_wcs, plane_intersection_wcs, plane_intersection_local, frame_gray

    def detect_offline(self, result_2d, frame_gray):
        result = self.detector.update_and_detect(result_2d, frame_gray,
                                                 apply_refraction_correction=False)

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

        return plane_intersection, eye_pos_world, gaze_ray, result
