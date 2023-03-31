from abc import ABC, abstractmethod

import numpy as np


class Preprocessor(ABC):
    @abstractmethod
    def preprocess_points(
        self,
        raw_x: np.ndarray,
        raw_y: np.ndarray,
        raw_z: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        pass
