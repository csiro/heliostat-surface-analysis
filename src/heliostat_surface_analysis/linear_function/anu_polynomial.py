import numpy as np

from heliostat_surface_analysis.linear_function.linear_function import LinearFunction


class ANUPolynomial(LinearFunction):
    def __init__(self):
        self.formula = "z = ax^2*y^2 + bx^2*y + cx^2 + dxy^2 + exy + fx + gy^2 + hy + i"
        self.terms = [
            lambda x, y: x**2 * y**2,
            lambda x, y: x**2 * y,
            lambda x, y: x**2,
            lambda x, y: x * y**2,
            lambda x, y: x * y,
            lambda x, y: x,
            lambda x, y: y**2,
            lambda x, y: y,
            lambda x, y: x * 0 + 1,
        ]
        self.df_dx_terms = [
            lambda x, y: 2 * x * y**2,
            lambda x, y: 2 * x * y,
            lambda x, y: 2 * x,
            lambda x, y: y**2,
            lambda x, y: y,
            lambda x, y: 0 * x + 1,
            lambda x, y: 0 * x,
            lambda x, y: 0 * x,
            lambda x, y: 0 * x,
        ]
        self.df_dy_terms = [
            lambda x, y: 2 * y * x**2,
            lambda x, y: x**2,
            lambda x, y: 0 * x,
            lambda x, y: 2 * y * x,
            lambda x, y: x,
            lambda x, y: 0 * x,
            lambda x, y: 2 * y,
            lambda x, y: 0 * x + 1,
            lambda x, y: 0 * x,
        ]
