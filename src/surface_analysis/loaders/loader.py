from abc import ABC, abstractmethod

import numpy as np


class Loader(ABC):
    @abstractmethod
    def load_points(file_path: str) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Load a point cloud x, y, z as Nx1 arrays
        """
        pass
