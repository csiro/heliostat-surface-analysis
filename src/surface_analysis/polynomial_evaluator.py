import numpy as np


class PolynomialEvaluator:
    def eval_centred_circular_paraboloid(coeff: list[float]) -> float:
        """
        z = a(x^2 + y^2)
        """
        def eval_poly(vec: np.ndarray):
            return (
                coeff[0] * (vec[0] ** 2 + vec[1] ** 2)
            )
        return eval_poly

    # def eval_centred_circular_paraboloid_normal(coeff: list[float]) -> float:
    #     """
    #     z = a(x^2 + y^2)
    #     dz/dx = 2ax
    #     dz/dy = 2ay
    #     n = [2ax, 2ay, -1]
    #     """
    #     def eval_poly(vec: np.ndarray):
    #         # zx = 2*coeff[0]*vec[0]
    #         # zy = 2*coeff[0]*vec[1]
    #         # n = [zx, zy, -1]
    #         # return (
    #         #     unit version of n
    #         # )
    #     return eval_poly

    def eval_centred_circular_paraboloid_with_z_offset(coeff: list[float]) -> float:
        """
        z = a(x^2 + y^2) + d
        """
        def eval_poly(vec: np.ndarray):
            return (
                coeff[0] * (vec[0] ** 2 + vec[1] ** 2)
                + coeff[1]
            )
        return eval_poly

    def eval_circular_paraboloid(coeff: list[float]) -> float:
        """
        z = a(x^2 + y^2) + bx + cy + d
        """
        def eval_poly(vec: np.ndarray):
            return (
                coeff[0] * (vec[0] ** 2 + vec[1] ** 2)
                + coeff[1] * vec[0]
                + coeff[2] * vec[1]
                + coeff[3]
            )
        return eval_poly

    def eval_elliptic_paraboloid(coeff: list[float]) -> float:
        """
        z = ax^2 + bx + cy^2 + dy + e
        """
        def eval_poly(vec: np.ndarray):
            return (
                coeff[0] * vec[0] ** 2
                + coeff[1] * vec[0]
                + coeff[2] * vec[1] ** 2
                + coeff[3] * vec[1]
                + coeff[4]
            )
        return eval_poly

    def eval_general_paraboloid(coeff: list[float]) -> float:
        """
        z = ax^2 + bx + cy^2 + dy + exy + f
        """
        def eval_poly(vec: np.ndarray):
            return (
                coeff[0] * vec[0] ** 2
                + coeff[1] * vec[0]
                + coeff[2] * vec[1] ** 2
                + coeff[3] * vec[1]
                + coeff[4] * vec[0] * vec[1]
                + coeff[5]
            )
        return eval_poly

    def eval_high_order_poly(coeff: list[float]) -> float:
        """
        z = ax^2y^2 + bx^2y + cx^2 + dxy^2 + exy + fx + gy^2 + hy + i
        """
        def eval_poly(vec: np.ndarray):
            return (
                coeff[0] * vec[0] ** 2 * vec[1] ** 2
                + coeff[1] * vec[0] ** 2 * vec[1]
                + coeff[2] * vec[0] ** 2
                + coeff[3] * vec[0] * vec[1] ** 2
                + coeff[4] * vec[0] * vec[1]
                + coeff[5] * vec[0]
                + coeff[6] * vec[1] ** 2
                + coeff[7] * vec[1]
                + coeff[8]
            )
        return eval_poly