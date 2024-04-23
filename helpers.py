import numpy as np


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
    def matmul(cls, v1, v2, pad=False, padBy=1.0):
        if pad is True:
            return np.matmul(v1, np.append(v2, padBy))[:-1]
        return np.matmul(v1, v2)
