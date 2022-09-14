from typing import Callable

import numpy as np


class LinearFunctionAssembler:
    def assemble_linear_function(
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
            A = np.hstack(evaluated_terms)
            return np.matmul(A, coeffs)

        return assembled_function

    def assemble_normal_function(
        self,
        gradient_func_x: Callable[[np.ndarray, np.ndarray], np.ndarray],
        gradient_func_y: Callable[[np.ndarray, np.ndarray], np.ndarray],
    ) -> Callable[[np.ndarray, np.ndarray], np.ndarray]:
        """
        Make z component equal 1
        x component is then -dz/dx
        y component is then -dz/dy
        """
        def assembled_function(x: np.ndarray, y: np.ndarray) -> np.ndarray:
            nx = -1 * gradient_func_x(x, y)
            ny = -1 * gradient_func_y(x, y)
            nz = np.ones(x.shape)
            return np.hstack([nx, ny, nz])

        return assembled_function
