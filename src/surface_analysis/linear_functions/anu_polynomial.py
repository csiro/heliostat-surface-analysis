import numpy as np

from surface_analysis.linear_functions.linear_function import LinearFunction


class ANUPolynomial(LinearFunction):
    def __init__(self):
        self.name = "anu_polynomial"
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

    def get_offsets(self, coeffs: np.ndarray) -> tuple[float, float, float]:
        # Can't get offsets for this complex of a polynomial
        return 0, 0, 0
