from typing import Callable

import numpy as np


class LinearLeastSquaresFitter:
    def fit_linear_function(
        self,
        x: np.ndarray,
        y: np.ndarray,
        z: np.ndarray,
        terms: list[Callable[[np.ndarray, np.ndarray], np.ndarray]],
    ) -> list[float]:
        """
        Fits the "term" functions to the data z
        """
        evaluated_terms = [term(x, y) for term in terms]
        A = np.hstack(evaluated_terms)
        coeffs, r, rank, s = np.linalg.lstsq(A, z, rcond=None)
        return coeffs

    def assemble_linear_function(
        self,
        terms: list[Callable[[np.ndarray, np.ndarray], np.ndarray]],
        coeffs: np.ndarray
    ) -> Callable[[np.ndarray, np.ndarray], np.ndarray]:
        """
        Put together the terms and coefficients to make the whole function.
        e.g. for single point
        coeffs: a, b
        terms: f1(x, y), f2(x, y)
        result: z = a*f1 + b*f2
        e.g. for arrays 
        coeffs: C
        terms: F1(X, Y) etc.
        results: Z = [F1(X, Y) F2(X, Y) F3(X, Y)]x[C]
        """
        def assembled_function(x: np.ndarray, y: np.ndarray) -> np.ndarray:
            evaluated_terms = [term(x, y) for term in terms]
            A = np.hstack(evaluated_terms)
            return np.matmul(A, coeffs)

        return assembled_function

"""
Example Code

    x = np.array([
        [0],
        [1],
        [2]
    ])
    y = np.array([
        [1],
        [0],
        [0]
    ])
    z = np.array([
        [1],
        [1],
        [4]
    ])
    terms = [
        lambda x, y: x**2,
        lambda x, y: y**2,
        lambda x, y: x * 0 + 1
    ]

    fitter = LinearLeastSquaresFitter()
    coeff = fitter.fit_linear_function(x, y, z, terms)
    print(coeff)
"""