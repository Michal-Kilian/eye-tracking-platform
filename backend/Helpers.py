import numpy as np
import sys
from scipy.spatial.transform import Rotation


class MathHelpers:
    @classmethod
    def cross_product(cls, a: np.ndarray, b: np.ndarray) -> np.ndarray:
        return np.cross(a, b)

    @classmethod
    def normalize(cls, v):
        return v / cls.magnitude(v)

    @classmethod
    def magnitude(cls, v):
        return np.sqrt(cls.sqr_magnitude(v))

    @classmethod
    def sqr_magnitude(cls, v):
        return cls.matmul(v, v)

    @classmethod
    def matmul(cls, v1, v2, pad=False, pad_by=1.0):
        if pad is True:
            return np.matmul(v1, np.append(v2, pad_by))[:-1]
        return np.matmul(v1, v2)

    @classmethod
    def map_value(cls, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    @classmethod
    def transform(cls, p, position, rot_mat):
        return cls.rotate(p, rot_mat) + position

    @classmethod
    def inverse_transform(cls, p, position, rot_mat):
        return (p - position) @ rot_mat

    @classmethod
    def rotate(cls, p, rot_mat):
        return p @ rot_mat.T

    @classmethod
    def intersect_plane(cls, n, p0, l0, ll):
        denom = cls.matmul(-n, ll)
        if denom > sys.float_info.min:
            p0l0 = p0 - l0
            t = cls.matmul(p0l0, -n) / denom
            return t
        return -1.0

    @classmethod
    def get_point(cls, ray, distance):
        return ray[0] + ray[1] * distance

    @classmethod
    def euler_to_rot(cls, theta, degrees=True):
        r = Rotation.from_euler("zxy", (theta[2], theta[0], theta[1]), degrees)
        return r.as_matrix()

    @classmethod
    def convert_to_uv(cls, vec, size_x, size_y, flip_y=True, include_outliers=False):
        x = (vec[0] + size_x / 2) / size_x
        y = (vec[1] + size_y / 2) / size_y
        if flip_y:
            y = 1 - y

        if not include_outliers:
            if x < 0 or x > 1 or y < 0 or y > 1:
                return None
        return np.array([x, y])

    @classmethod
    def convert_to_uv_offline(cls, vec, size_x, size_y, flip_y=True, include_outliers=False):
        x = (vec[0] + size_x / 2) / size_x
        y = (vec[2] + size_y / 2) / size_y
        if flip_y:
            y = 1 - y

        if not include_outliers:
            if x < 0 or x > 1 or y < 0 or y > 1:
                return None
        return x, y

    @classmethod
    def convert_uv_to_px(cls, uv_data, width, height):
        return int(uv_data[0] * width), int(uv_data[1] * height)

    @classmethod
    def lerp(cls, a, b, t):
        return (1 - t) * a + t * b
