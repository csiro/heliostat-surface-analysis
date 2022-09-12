from typing import Callable

import numpy as np


class LinearFunctionAssembler:
    def assemble_linear_function(
        self,
        terms: list[Callable[[np.ndarray, np.ndarray], np.ndarray]],
        coeffs: np.ndarray,
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

    def assemble_gradient_function(
        self,
        x_terms: list[Callable[[np.ndarray, np.ndarray], np.ndarray]],
        y_terms: list[Callable[[np.ndarray, np.ndarray], np.ndarray]],
        coeffs: np.ndarray,
    ) -> tuple[
        Callable[[np.ndarray, np.ndarray], np.ndarray],
        Callable[[np.ndarray, np.ndarray], np.ndarray],
    ]:
        """
        Takes the linear terms that make up the dz/dx function and the dz/dy function.
        Takes the coefficients of z = a * f1(x, y) + b * f2(x, y) ...
        Returns dz/dx function that can take x and y arrays
        Returns dz/dy function that can take x and y arrays
        Coefficients are from the base (non-derived function), and the x_terms
        and y_terms already have the constants incorporated.
        """
        dz_dx_func = self.assemble_linear_function(x_terms, coeffs)
        dz_dy_func = self.assemble_linear_function(y_terms, coeffs)
        return (dz_dx_func, dz_dy_func)

    def assemble_normal_function(
        self,
        gradient_func_x: Callable[[np.ndarray, np.ndarray], np.ndarray],
        gradient_func_y: Callable[[np.ndarray, np.ndarray], np.ndarray],
    ) -> Callable[[np.ndarray, np.ndarray], np.ndarray]:
        """
        Make the z component equal to 1
        x component is then -dz/dx
        y component is then -dz/dy
        """
        def assembled_function(x: np.ndarray, y: np.ndarray) -> np.ndarray:
            nx = -1 * gradient_func_x(x, y)
            ny = -1 * gradient_func_y(x, y)
            nz = np.ones(x.shape)
            return np.hstack([nx, ny, nz])

        return assembled_function
