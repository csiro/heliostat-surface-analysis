from abc import ABC, abstractmethod

import numpy as np
import pandas as pd


class Analyzer(ABC):
    @abstractmethod
    def analyze(
        self,
        x: np.ndarray,
        y: np.ndarray,
        z: np.ndarray,
        scan_name: str
    ) -> pd.DataFrame:
        pass
