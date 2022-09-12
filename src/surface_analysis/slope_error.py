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
        and the ideal normals at each point as provided by ideal_normal_func.
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

    def slope_error_weighted_mean(
        self,
        x: np.ndarray,
        y: np.ndarray,
        measured_normals: np.ndarray,
        weights: np.ndarray,
        ideal_normal_func: Callable[[np.ndarray], np.ndarray],
    ) -> float:
        """
        Finds the mean slope error between the measured normals
        and the normals provided by ideal_normal_func.
        Weights the mean by the provided weights.
        """
        angular_differences = self.calculate_angular_differences(
            x,
            y,
            measured_normals,
            ideal_normal_func,
        )
        weighted_angular_differences = angular_differences * weights
        return np.sum(weighted_angular_differences) / np.sum(weights)

    def slope_error_weighted_rms(
        self,
        x: np.ndarray,
        y: np.ndarray,
        measured_normals: np.ndarray,
        weights: np.ndarray,
        ideal_normal_func: Callable[[np.ndarray], np.ndarray],
    ) -> float:
        """
        Finds the RMS slope error between the measured normals
        and the normals provided by ideal_normal_func.
        Weights the mean step by the provided weights.
        """
        angular_differences = self.calculate_angular_differences(
            x,
            y,
            measured_normals,
            ideal_normal_func,
        )
        weighted_squared_angular_differences = np.square(angular_differences) * weights
        mean_square = np.sum(weighted_squared_angular_differences) / np.sum(weights)
        return np.sqrt(mean_square)
