from typing import Callable

import numpy as np

from surface_analysis.linear_functions.linear_function import LinearFunction
from surface_analysis.linear_functions.linear_function_assembler import LinearFunctionAssembler 
from surface_analysis.linear_functions.linear_function_creator import LinearFunctionCreator 
from surface_analysis.slope_error import SlopeErrorCalculator


def ordinary_least_squares_objective(x, y, z):
    lfc = LinearFunctionCreator()
    poly = lfc.circular_paraboloid()
    assembler = LinearFunctionAssembler()

    def objective_function(coeffs, grad):
        coeffs = coeffs.reshape((-1, 1))
        f = assembler.assemble_linear_function(poly.terms, coeffs)
        residuals = z - f(x, y)
        return np.sum(np.square(residuals))

    return objective_function

def min_mean_slope_error_objective(x_c, y_c, n, area):
    lfc = LinearFunctionCreator()
    poly = lfc.circular_paraboloid()
    assembler = LinearFunctionAssembler()
    sec = SlopeErrorCalculator()

    def objective_function(coeffs, grad):
        coeffs = coeffs.reshape((-1, 1))
        df_dx = assembler.assemble_linear_function(poly.df_dx_terms, coeffs)
        df_dy = assembler.assemble_linear_function(poly.df_dy_terms, coeffs)
        normal_func = assembler.assemble_normal_function(df_dx, df_dy)
        angular_differences = sec.calculate_angular_differences(x_c, y_c, n, normal_func)
        return sec.calculate_weighted_mean(angular_differences, area)

    return objective_function




def angular_error(
    x: np.ndarray,
    y: np.ndarray,
    n: np.ndarray,
    linear_function: LinearFunction,
    comparitor: Callable[[np.ndarray], np.ndarray],
    aggregator: Callable[[np.ndarray], np.ndarray],
):
    sec = SlopeErrorCalculator()

    def objective_function(coeffs, grad):
        coeffs = coeffs.reshape((-1, 1))
        normal_func = linear_function.assemble_normal_function()
        angular_differences = sec.calculate_angular_differences(x, y, n, normal_func)
        return aggregator(angular_differences)

    return objective_function



# def angular_error(
#     x: np.ndarray,
#     y: np.ndarray,
#     n: np.ndarray,
#     linear_function: LinearFunction,
#     comparitor: Callable[[np.ndarray], np.ndarray],
#     aggregator: Callable[[np.ndarray], np.ndarray],
# ):
#     sec = SlopeErrorCalculator()

#     def objective_function(coeffs, grad):
#         coeffs = coeffs.reshape((-1, 1))
#         normal_func = linear_function.assemble_normal_function()
#         angular_differences = sec.calculate_angular_differences(x, y, n, normal_func)
#         return aggregator(angular_differences)

#     return objective_function
