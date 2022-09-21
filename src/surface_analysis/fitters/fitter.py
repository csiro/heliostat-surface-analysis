from typing import Callable
from abc import ABC, abstractmethod

import numpy as np
import nlopt

from surface_analysis.objectives.linear_objective_function import LinearObjectiveFunction


class Fitter(ABC):
    @abstractmethod
    def fit(self) -> np.ndarray:
        return


class LinearLeastSquaresFitter(Fitter):
    def __init__(
        self,

        terms: list[Callable[[np.ndarray, np.ndarray], np.ndarray]],
    ) -> None:
        self.terms = terms

    def fit(
        self,
        x: np.ndarray,
        y: np.ndarray,
        z: np.ndarray,
    ) -> np.ndarray:
        evaluated_terms = [term(x, y) for term in self.terms]
        A = np.hstack(evaluated_terms)
        coeffs, r, rank, s = np.linalg.lstsq(A, z, rcond=None)
        return coeffs


class NonLinearFitter(Fitter):
    def __init__( 
        self,
        dimensions: int,
        obj: LinearObjectiveFunction,
        lower_bound: list[float],
        upper_bound: list[float],
        initial_guess: list[float],
    ):
        self.dimensions = dimensions
        self.obj = obj
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.initial_guess = initial_guess

    def fit(self) -> np.ndarray:
        opt = nlopt.opt(nlopt.LN_COBYLA, self.dimensions)
        opt.set_lower_bounds(self.lower_bound)
        opt.set_upper_bounds(self.upper_bound)
        opt.set_min_objective(self.obj.evaluate)
        opt.set_xtol_rel(1e-6)
        xopt = opt.optimize(self.initial_guess)
        return xopt.reshape((-1, 1))
