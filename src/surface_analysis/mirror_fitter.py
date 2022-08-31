import pandas as pd
import numpy as np

class MirrorFitter:
    @staticmethod
    def fit_circular_paraboloid(points: pd.DataFrame) -> list[float]:
        """
        Fit a circular paraboloid to the data.
        z = a(x^2 + y^2) + bx + cy + d
        """
        x = np.array(points["x"])
        y = np.array(points["y"])
        z = np.array(points["z"])

        A = np.array([x**2 + y**2, x, y, x*0+1]).T

        coeff, r, rank, s = np.linalg.lstsq(A, z, rcond=None)
        return coeff

    @staticmethod
    def fit_elliptic_paraboloid(points: pd.DataFrame) -> list[float]:
        """
        Fit an elliptic paraboloid to the data.
        z = ax^2 + bx + cy^2 + dy + c
        """
        x = np.array(points["x"])
        y = np.array(points["y"])
        z = np.array(points["z"])

        A = np.array([x**2, x, y**2, y, x*0+1]).T

        coeff, r, rank, s = np.linalg.lstsq(A, z, rcond=None)
        return coeff

    @staticmethod
    def fit_general_paraboloid(points: pd.DataFrame) -> float:
        """
        Fit an general paraboloid to the data.
        z = ax^2 + bx + cy^2 + dy + exy + f
        """
        x = np.array(points["x"])
        y = np.array(points["y"])
        z = np.array(points["z"])

        A = np.array([x**2, x, y**2, y, x*y, x*0+1]).T

        coeff, r, rank, s = np.linalg.lstsq(A, z, rcond=None)
        return coeff

    @staticmethod
    def fit_higher_order_terms(points: pd.DataFrame) -> float:
        """
        Fit higher order terms to the data.
        z = ax^2y^2 + bx^2y + cx^2 + dxy^2 + exy + fx + gy^2 + hy + i
        """
        x = np.array(points["x"])
        y = np.array(points["y"])
        z = np.array(points["z"])

        A = np.array([x**2*y**2, x**2*y, x**2, x*y**2, x*y, x, y**2, y, x*0+1]).T

        coeff, r, rank, s = np.linalg.lstsq(A, z, rcond=None)
        return coeff
