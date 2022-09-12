from typing import Callable

import numpy as np


class GradientTerms:
    def centred_circular_paraboloid(
        self,
    ) -> tuple[
        list[Callable[[np.ndarray, np.ndarray], np.ndarray]],
        list[Callable[[np.ndarray, np.ndarray], np.ndarray]],
    ]:
        dz_dx = [
            lambda x, y: 2 * x,
        ]
        dz_dy = [
            lambda x, y: 2 * y,
        ]
        return (dz_dx, dz_dy)

    def centred_circular_paraboloid_with_z_offset(
        self,
    ) -> tuple[
        list[Callable[[np.ndarray, np.ndarray], np.ndarray]],
        list[Callable[[np.ndarray, np.ndarray], np.ndarray]],
    ]:
        dz_dx = [
            lambda x, y: 2 * x,
            lambda x, y: x * 0,
        ]
        dz_dy = [
            lambda x, y: 2 * y,
            lambda x, y: x * 0,
        ]
        return (dz_dx, dz_dy)

    def circular_paraboloid(
        self,
    ) -> tuple[
        list[Callable[[np.ndarray, np.ndarray], np.ndarray]],
        list[Callable[[np.ndarray, np.ndarray], np.ndarray]],
    ]:
        dz_dx = [
            lambda x, y: 2 * x,
            lambda x, y: x * 0 + 1,
            lambda x, y: x * 0,
            lambda x, y: x * 0,
        ]
        dz_dy = [
            lambda x, y: 2 * y,
            lambda x, y: x * 0,
            lambda x, y: x * 0 + 1,
            lambda x, y: x * 0,
        ]
        return (dz_dx, dz_dy)

    def general_paraboloid(
        self,
    ) -> tuple[
        list[Callable[[np.ndarray, np.ndarray], np.ndarray]],
        list[Callable[[np.ndarray, np.ndarray], np.ndarray]],
    ]:
        dz_dx = [
            lambda x, y: 2 * x,
            lambda x, y: x * 0 + 1,
            lambda x, y: x * 0,
            lambda x, y: x * 0,
            lambda x, y: y,
            lambda x, y: x * 0,
        ]
        dz_dy = [
            lambda x, y: x * 0,
            lambda x, y: x * 0,
            lambda x, y: 2 * y,
            lambda x, y: x * 0 + 1,
            lambda x, y: x,
            lambda x, y: x * 0,
        ]
        return (dz_dx, dz_dy)
