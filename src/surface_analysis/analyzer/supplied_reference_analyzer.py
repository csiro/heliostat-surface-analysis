import numpy as np
import pandas as pd

from surface_analysis.linear_function.linear_function import LinearFunction
from surface_analysis.analyser.analyser import Analyser
from surface_analysis.measured_surface import MeasuredSurface


class SuppliedReferenceAnalyser(Analyser):
    def analyse(
        self,
        points: np.ndarray,
        supplied_reference: LinearFunction
    ) -> pd.DataFrame:
        pass
