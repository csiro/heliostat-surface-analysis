from typing import Callable

import numpy as np


class LinearTerms:
    def centred_circular_paraboloid(
        self,
    ) -> list[Callable[[np.ndarray, np.ndarray], np.ndarray]]:
        return [
            lambda x, y: x**2 + y**2,
        ]

    def centred_circular_paraboloid_with_z_offset(
        self,
    ) -> list[Callable[[np.ndarray, np.ndarray], np.ndarray]]:
        return [
            lambda x, y: x**2 + y**2,
            lambda x, y: x * 0 + 1,
        ]

    def circular_paraboloid(
        self,
    ) -> list[Callable[[np.ndarray, np.ndarray], np.ndarray]]:
        return [
            lambda x, y: x**2 + y**2,
            lambda x, y: x,
            lambda x, y: y,
            lambda x, y: x * 0 + 1,
        ]

    def elliptic_paraboloid(
        self,
    ) -> list[Callable[[np.ndarray, np.ndarray], np.ndarray]]:
        return [
            lambda x, y: x**2,
            lambda x, y: x,
            lambda x, y: y**2,
            lambda x, y: y,
            lambda x, y: x * 0 + 1,
        ]

    def general_paraboloid(
        self,
    ) -> list[Callable[[np.ndarray, np.ndarray], np.ndarray]]:
        return [
            lambda x, y: x**2,
            lambda x, y: x,
            lambda x, y: y**2,
            lambda x, y: y,
            lambda x, y: x * y,
            lambda x, y: x * 0 + 1,
        ]

    def high_order_poly(
        self,
    ) -> list[Callable[[np.ndarray, np.ndarray], np.ndarray]]:
        return [
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
