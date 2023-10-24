from typing import Callable,Tuple
from abc import ABC, abstractmethod

import numpy as np

from surface_analysis.linear_function.linear_function import LinearFunction
from surface_analysis.comparitor.comparitor import Comparitor, DifferenceComparitor, AngularDifferenceComparitor
from surface_analysis.aggregator.aggregator import Aggregator, SquaredSumAggregator, WeightedRMSAggregator

class LinearObjectiveFunction(ABC):
    @abstractmethod
    def evaluate(self, coeffs: np.ndarray, grad) -> float:
        pass

    def compare_data_with_function(
        self,
        x: np.ndarray,
        y: np.ndarray,
        z: np.ndarray,
        evaluator: Callable[[np.ndarray], np.ndarray],
        comparitor: Comparitor,
        aggregator: Aggregator,
    ) -> float:
        values = evaluator(x, y)
        differences = comparitor.compare(values, z)
        return aggregator.aggregate(differences)


class SquaredDistanceObjectiveFunction(LinearObjectiveFunction):
    def __init__(
        self,
        x: np.ndarray,
        y: np.ndarray,
        z: np.ndarray,
        linear_func: LinearFunction,
    ) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.linear_func = linear_func

    def evaluate(self, coeffs: np.ndarray, grad) -> float:
        coeffs = coeffs.reshape((-1, 1))
        f = self.linear_func.assemble_function(coeffs)
        return self.compare_data_with_function(
            self.x,
            self.y,
            self.z,
            f,
            DifferenceComparitor(),
            SquaredSumAggregator(self.area),
        )

class SlopeErrorObjectiveFunction(LinearObjectiveFunction):
    def __init__(
        self,
        x: np.ndarray,
        y: np.ndarray,
        n: np.ndarray,
        area: np.ndarray,
        linear_func: LinearFunction,
    ) -> None:
        self.x = x
        self.y = y
        self.n = n
        self.area = area
        self.linear_func = linear_func
    
    def evaluate(self, coeffs: np.ndarray, grad) -> float:
        coeffs = coeffs.reshape((-1, 1))
        f_n = self.linear_func.assemble_normal_function(coeffs)
        return self.compare_data_with_function(
            self.x,
            self.y,
            self.n,
            f_n,
            AngularDifferenceComparitor(),
            WeightedRMSAggregator(self.area),
        )

