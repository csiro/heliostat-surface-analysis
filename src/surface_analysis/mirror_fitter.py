from typing import Callable
import pandas as pd
import numpy as np


class MirrorFitter:
    @staticmethod
    def fit_centred_circular_paraboloid(
        points: pd.DataFrame,
    ) -> tuple(list[float], Callable[[float, float], float]):
        """
        Fit a centred circular paraboloid to the data.
        z = a(x^2 + y^2)
        """
        x = np.array(points["x"])
        y = np.array(points["y"])
        z = np.array(points["z"])

        A = np.array([x**2 + y**2]).T

        coeff, r, rank, s = np.linalg.lstsq(A, z, rcond=None)

        def eval_centred_circular_paraboloid(vec: np.ndarray) -> float:
            return coeff[0] * (vec[0] ** 2 + vec[1] ** 2)

        return coeff, eval_centred_circular_paraboloid

    @staticmethod
    def fit_circular_paraboloid(
        points: pd.DataFrame,
    ) -> tuple(list[float], Callable[[float, float], float]):
        """
        Fit a circular paraboloid to the data.
        z = a(x^2 + y^2) + bx + cy + d
        """
        x = np.array(points["x"])
        y = np.array(points["y"])
        z = np.array(points["z"])

        A = np.array(
            [
                x**2 + y**2,
                x,
                y,
                x * 0 + 1,
            ]
        ).T

        coeff, r, rank, s = np.linalg.lstsq(A, z, rcond=None)

        def eval_circular_paraboloid(vec: np.ndarray) -> float:
            return (
                coeff[0] * (vec[0] ** 2 + vec[1] ** 2)
                + coeff[1] * vec[0]
                + coeff[2] * vec[1]
                + coeff[3]
            )

        return coeff, eval_circular_paraboloid

    @staticmethod
    def fit_elliptic_paraboloid(
        points: pd.DataFrame,
    ) -> tuple(list[float], Callable[[float, float], float]):
        """
        Fit an elliptic paraboloid to the data.
        z = ax^2 + bx + cy^2 + dy + e
        """
        x = np.array(points["x"])
        y = np.array(points["y"])
        z = np.array(points["z"])

        A = np.array(
            [
                x**2,
                x,
                y**2,
                y,
                x * 0 + 1,
            ]
        ).T

        coeff, r, rank, s = np.linalg.lstsq(A, z, rcond=None)

        def eval_elliptic_paraboloid(vec: np.ndarray) -> float:
            return (
                coeff[0] * vec[0] ** 2
                + coeff[1] * vec[0]
                + coeff[2] * vec[1] ** 2
                + coeff[3] * vec[1]
                + coeff[4]
            )

        return coeff, eval_elliptic_paraboloid

    @staticmethod
    def fit_general_paraboloid(
        points: pd.DataFrame,
    ) -> tuple(list[float], Callable[[float, float], float]):
        """
        Fit an general paraboloid to the data.
        z = ax^2 + bx + cy^2 + dy + exy + f
        """
        x = np.array(points["x"])
        y = np.array(points["y"])
        z = np.array(points["z"])

        A = np.array(
            [
                x**2,
                x,
                y**2,
                y,
                x * y,
                x * 0 + 1,
            ]
        ).T

        coeff, r, rank, s = np.linalg.lstsq(A, z, rcond=None)

        def eval_general_paraboloid(vec: np.ndarray) -> float:
            return (
                coeff[0] * vec[0] ** 2
                + coeff[1] * vec[0]
                + coeff[2] * vec[1] ** 2
                + coeff[3] * vec[1]
                + coeff[4] * vec[0] * vec[1]
                + coeff[5]
            )

        return coeff, eval_general_paraboloid

    @staticmethod
    def fit_high_order_poly(
        points: pd.DataFrame,
    ) -> tuple(list[float], Callable[[float, float], float]):
        """
        Fit higher order terms to the data.
        z = ax^2y^2 + bx^2y + cx^2 + dxy^2 + exy + fx + gy^2 + hy + i
        """
        x = np.array(points["x"])
        y = np.array(points["y"])
        z = np.array(points["z"])

        A = np.array(
            [
                x**2 * y**2,
                x**2 * y,
                x**2,
                x * y**2,
                x * y,
                x,
                y**2,
                y,
                x * 0 + 1,
            ]
        ).T

        coeff, r, rank, s = np.linalg.lstsq(A, z, rcond=None)

        def eval_high_order_poly(vec: np.ndarray) -> float:
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

        return coeff, eval_high_order_poly
