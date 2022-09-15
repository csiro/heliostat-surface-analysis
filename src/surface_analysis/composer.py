from typing import Callable

import numpy as np


def compare_data_with_function(
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    evaluator: Callable[[np.ndarray], np.ndarray],
    comparitor: Callable[[np.ndarray], np.ndarray],
    aggregator: Callable[[np.ndarray], np.ndarray],
):
    values = evaluator(x, y)
    differences = comparitor(z, values)
    return aggregator(differences)
