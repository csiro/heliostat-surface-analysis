from abc import ABC, abstractmethod

import pandas as pd

from surface_analysis.measured_surface import MeasuredSurface


class Analyser(ABC):
    @abstractmethod
    def analyse(
        self,
        surface: MeasuredSurface,
        scan_name: str,
        output_dir: str,
        width: float,
        height: float,
        design_focal_length: float,
    ) -> pd.DataFrame:
        pass
