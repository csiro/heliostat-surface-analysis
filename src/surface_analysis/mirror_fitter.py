from typing import Callable

import pandas as pd
import numpy as np

from surface_analysis.polynomial_evaluator import PolynomialEvaluator


class MirrorFitter:
    @staticmethod
    def fit_centred_circular_paraboloid(
        points: pd.DataFrame,
    ) -> tuple[list[float], Callable[[float, float], float]]:
        """
        Fit a centred circular paraboloid to the data.
        z = a(x^2 + y^2)
        """
        x = np.array(points["x"])
        y = np.array(points["y"])
        z = np.array(points["z"])

        A = np.array([x**2 + y**2]).T

        coeff, r, rank, s = np.linalg.lstsq(A, z, rcond=None)

        return coeff, PolynomialEvaluator.eval_centred_circular_paraboloid(coeff)

    @staticmethod
    def fit_centred_circular_paraboloid_with_z_offset(
        points: pd.DataFrame,
    ) -> tuple[list[float], Callable[[float, float], float]]:
        """
        Fit a circular paraboloid with z offset to the data.
        z = a(x^2 + y^2) + d
        """
        x = np.array(points["x"])
        y = np.array(points["y"])
        z = np.array(points["z"])

        A = np.array(
            [
                x**2 + y**2,
                x * 0 + 1,
            ]
        ).T

        coeff, r, rank, s = np.linalg.lstsq(A, z, rcond=None)

        return coeff, PolynomialEvaluator.eval_centred_circular_paraboloid_with_z_offset(coeff)

    @staticmethod
    def fit_circular_paraboloid(
        points: pd.DataFrame,
    ) -> tuple[list[float], Callable[[float, float], float]]:
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

        return coeff, PolynomialEvaluator.eval_circular_paraboloid(coeff)

    @staticmethod
    def fit_elliptic_paraboloid(
        points: pd.DataFrame,
    ) -> tuple[list[float], Callable[[float, float], float]]:
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

        return coeff, PolynomialEvaluator.eval_elliptic_paraboloid(coeff)

    @staticmethod
    def fit_general_paraboloid(
        points: pd.DataFrame,
    ) -> tuple[list[float], Callable[[float, float], float]]:
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

        return coeff, PolynomialEvaluator.eval_general_paraboloid(coeff)

    @staticmethod
    def fit_high_order_poly(
        points: pd.DataFrame,
    ) -> tuple[list[float], Callable[[float, float], float]]:
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

        return coeff, PolynomialEvaluator.eval_high_order_poly(coeff)

    @staticmethod
    def fit_1d_parabola_radially(
        points: pd.DataFrame,
    ) -> list[float]:
        """
        Transform the data to be in terms of only r and fit a 1d parabola to it.
        """
        x = np.array(points["x"])
        y = np.array(points["y"])
        r = np.sqrt(x**2 + y**2)
        z = np.array(points["z"])

        A = np.array(
            [
                r**2,
                r,
                r * 0 + 1,
            ]
        ).T

        coeff, r, rank, s = np.linalg.lstsq(A, z, rcond=None)

        return coeff
