from abc import ABC, abstractmethod

import numpy as np


class Mesher(ABC):
    @abstractmethod
    def points_to_facets(
        self,
        x: np.ndarray,
        y: np.ndarray,
        z: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        pass
