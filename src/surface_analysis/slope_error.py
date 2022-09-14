from typing import Callable

import numpy as np

from surface_analysis.vector_math import normalise_vectors


class SlopeErrorCalculator:
    def calculate_angular_differences(
        self,
        x: np.ndarray,
        y: np.ndarray,
        measured_normals: np.ndarray,
        ideal_normal_func: Callable[[np.ndarray, np.ndarray], np.ndarray],
    ) -> np.ndarray:
        """
        Computes the difference in angle between the measured normals
        and the normals provided by ideal_normal_func.
        """
        ideal_normals = ideal_normal_func(x, y)

        measured_unit_normals = normalise_vectors(measured_normals)
        ideal_unit_normals = normalise_vectors(ideal_normals)

        measured_dot_ideal = np.sum(
            measured_unit_normals * ideal_unit_normals,
            axis=1,
            keepdims=True,
        )
        # Computational precision can result in values slightly outside [-1, 1]
        measured_dot_ideal = np.clip(measured_dot_ideal, -1, 1)

        return np.arccos(measured_dot_ideal)

    def calculate_weighted_mean(self, values: np.ndarray, weights: np.ndarray) -> float:
        weighted_values = values * weights
        return np.sum(weighted_values) / np.sum(weights)

    def calculate_weighted_rms(self, values: np.ndarray, weights: np.ndarray) -> float:
        weighted_squared_values = np.square(values) * weights
        mean_square = np.sum(weighted_squared_values) / np.sum(weights)
        return np.sqrt(mean_square)
