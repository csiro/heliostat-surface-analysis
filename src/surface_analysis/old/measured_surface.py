from dataclasses import dataclass

import numpy as np


@dataclass
class MeasuredSurface:
    x: np.ndarray
    y: np.ndarray
    z: np.ndarray
    x_c: np.ndarray
    y_c: np.ndarray
    z_c: np.ndarray
    n: np.ndarray
    area: np.ndarray
