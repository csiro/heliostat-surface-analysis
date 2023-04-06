from typing import Callable
from abc import ABC

import numpy as np


class LinearFunction(ABC):
    formula: str
    terms: list[Callable[[np.ndarray, np.ndarray], np.ndarray]]
    df_dx_terms: list[Callable[[np.ndarray, np.ndarray], np.ndarray]]
    df_dy_terms: list[Callable[[np.ndarray, np.ndarray], np.ndarray]]

    def __str__(self) -> str:
        return type(self).__name__

    def assemble_function(
        self,
        coeffs: np.ndarray,
    ) -> Callable[[np.ndarray, np.ndarray], np.ndarray]:
        return self.assemble_terms_and_coeffs(self.terms, coeffs)

    def assemble_normal_function(
        self,
        coeffs: np.ndarray,
    ) -> Callable[[np.ndarray, np.ndarray], np.ndarray]:
        """
        Make z component equal 1
        x component is then -dz/dx
        y component is then -dz/dy
        """
        df_dx = self.assemble_terms_and_coeffs(self.df_dx_terms, coeffs)
        df_dy = self.assemble_terms_and_coeffs(self.df_dy_terms, coeffs)

        def assembled_function(x: np.ndarray, y: np.ndarray) -> np.ndarray:
            nx = -1 * df_dx(x, y)
            ny = -1 * df_dy(x, y)
            nz = np.ones(x.shape)
            return np.hstack([nx, ny, nz])

        return assembled_function

    def assemble_terms_and_coeffs(
        self,
        terms: list[Callable[[np.ndarray, np.ndarray], np.ndarray]],
        coeffs: np.ndarray,
    ) -> Callable[[np.ndarray, np.ndarray], np.ndarray]:
        """
        Put together the term matrix and coefficient vector to make the whole function.
        e.g.
        coeff column vector: C = [a; b]
        term matrix: [F1(X, Y), F2(X, Y)]
        results: Z = [F1(X, Y) F2(X, Y)][C]
        """
        def assembled_function(x: np.ndarray, y: np.ndarray) -> np.ndarray:
            evaluated_terms = [term(x, y) for term in terms]
            F = np.hstack(evaluated_terms)
            return np.matmul(F, coeffs)

        return assembled_function

    # def get_offsets(self, coeffs: np.ndarray) -> tuple[float, float, float]:
    #     """
    #     For the given coefficients, calculate the x offset that would
    #     remove the plain "bx", "cy" and "e" terms.
    #     These summarise the x, y and z offset.
    #     """
    #     pass
