from typing import Callable

import numpy as np


class LinearLeastSquaresFitter:
    def fit_linear_function(
        self,
        x: np.ndarray,
        y: np.ndarray,
        z: np.ndarray,
        terms: list[Callable[[np.ndarray, np.ndarray], np.ndarray]],
    ) -> tuple[list[float], np.float64]:
        """
        Fits the "term" functions to the data z at the points (x, y)
        """
        evaluated_terms = [term(x, y) for term in terms]
        A = np.hstack(evaluated_terms)
        coeffs, r, rank, s = np.linalg.lstsq(A, z, rcond=None)
        return coeffs, r[0]
