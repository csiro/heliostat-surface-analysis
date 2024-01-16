from abc import ABC, abstractmethod

import numpy as np
import pandas as pd

from stl.mesh import Mesh


class Analyser(ABC):
    @abstractmethod
    def analyse(
        self,
        x: np.ndarray,
        y: np.ndarray,
        z: np.ndarray,
        mesh: Mesh,
        scan_name: str
    ) -> pd.DataFrame:
        pass
    @abstractmethod
    def get_coefficient_labels(self) -> list:
        pass
