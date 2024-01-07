import numpy as np

from heliostat_surface_analysis.linear_function.linear_function import LinearFunction

import typing

class CircularParaboloid(LinearFunction):
    def __init__(self):
        self.formula = "z = a(x^2 + y^2) + bx + cy + d"
        self.terms = [
            lambda x, y: x**2 + y**2,
            lambda x, y: x,
            lambda x, y: y,
            lambda x, y: x * 0 + 1,
        ]
        self.df_dx_terms = [
            lambda x, y: 2 * x,
            lambda x, y: 0 * x + 1,
            lambda x, y: 0 * x,
            lambda x, y: 0 * x,
        ]
        self.df_dy_terms = [
            lambda x, y: 2 * y,
            lambda x, y: 0 * x,
            lambda x, y: 0 * x + 1,
            lambda x, y: 0 * x,
        ]

    def get_offsets(self, coeffs: np.ndarray) -> typing.Tuple[float, float, float]:
        x_offset = coeffs[1, 0] / (2 * coeffs[0, 0])
        y_offset = coeffs[2, 0] / (2 * coeffs[0, 0])
        z_offset = -1 * (coeffs[1, 0]**2 + coeffs[2, 0]**2) / (4 * coeffs[0, 0]) + coeffs[3, 0]
        return np.array([x_offset, y_offset, z_offset])
