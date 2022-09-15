from typing import Callable

import numpy as np

from surface_analysis.linear_functions.linear_function import LinearFunction
from surface_analysis.comparitor import angular_difference, difference
from surface_analysis.aggregator import (
    create_weighted_mean_aggregator,
    create_weighted_rms_aggregator,
    create_squared_sum_aggregator,
)
from surface_analysis.composer import compare_data_with_function


def squared_z_distance_objective(
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    linear_func: LinearFunction,
) -> Callable[[np.ndarray, np.ndarray], float]:
    def objective_function(coeffs, grad):
        coeffs = coeffs.reshape((-1, 1))
        f = linear_func.assemble_function(coeffs)
        return compare_data_with_function(
            x,
            y,
            z,
            f,
            difference,
            create_squared_sum_aggregator(),
        )

    return objective_function


def mean_slope_error_objective(
    x: np.ndarray,
    y: np.ndarray,
    n: np.ndarray,
    area: np.ndarray,
    linear_func: LinearFunction,
) -> Callable[[np.ndarray, np.ndarray], float]:
    def objective_function(coeffs, grad):
        coeffs = coeffs.reshape((-1, 1))
        normal_function = linear_func.assemble_normal_function(coeffs)
        return compare_data_with_function(
            x,
            y,
            n,
            normal_function,
            angular_difference,
            create_weighted_mean_aggregator(area),
        )

    return objective_function


def rms_slope_error_objective(
    x: np.ndarray,
    y: np.ndarray,
    n: np.ndarray,
    area: np.ndarray,
    linear_func: LinearFunction,
) -> Callable[[np.ndarray, np.ndarray], float]:
    def objective_function(coeffs, grad):
        coeffs = coeffs.reshape((-1, 1))
        normal_function = linear_func.assemble_normal_function(coeffs)
        return compare_data_with_function(
            x,
            y,
            n,
            normal_function,
            angular_difference,
            create_weighted_rms_aggregator(area),
        )

    return objective_function
