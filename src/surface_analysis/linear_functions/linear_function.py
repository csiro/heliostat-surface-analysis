from dataclasses import dataclass
from typing import Callable

import numpy as np


@dataclass
class LinearFunction:
    name: str
    formula: str
    terms: list[Callable[[np.ndarray, np.ndarray], np.ndarray]]
    df_dx_terms: list[Callable[[np.ndarray, np.ndarray], np.ndarray]]
    df_dy_terms: list[Callable[[np.ndarray, np.ndarray], np.ndarray]]
