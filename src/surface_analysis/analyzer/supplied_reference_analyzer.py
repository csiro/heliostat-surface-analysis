from typing import Union, Optional, cast, Any

import numpy as np

from surface_analysis.linear_function.plane import Plane
from surface_analysis.linear_function.circular_paraboloid import CircularParaboloid
from surface_analysis.analyzer.analyzer import Analyzer
from surface_analysis.comparitor.comparitor import AngularDifferenceComparitor
from surface_analysis.fitter.fitter import LinearLeastSquaresFitter
from surface_analysis.mesh.default_mesher import DefaultMesher
from surface_analysis.plotter import Plotter
from surface_analysis.aggregator.aggregator import MeanAggregator
from surface_analysis.aggregator.aggregator import RMSAggregator


class SuppliedReferenceAnalyzer(Analyzer):
    def __init__(
        self,
        params: Optional[dict[str, Union[str, float]]]
    ):
        params = cast(dict[str, Union[str, float]], params)
        if params["surface"] == "flat":
            self.reference = Plane()
        else:
            self.reference = CircularParaboloid()

    def analyze(
        self,
        x: np.ndarray,
        y: np.ndarray,
        z: np.ndarray,
    ) -> dict[str, Any]:
        mesher = DefaultMesher()
        x_c, y_c, z_c, area, n = mesher.points_to_facets(x, y, z)

        fitter = LinearLeastSquaresFitter()
        coeffs = fitter.fit(self.reference.terms, x, y, z)
        f_n = self.reference.assemble_normal_function(coeffs)

        angle_comparitor = AngularDifferenceComparitor()
        slope_diffs = angle_comparitor.compare(n, f_n(x_c, y_c))

        mean_aggregator = MeanAggregator()
        rms_aggregator = RMSAggregator()
        slope_mean = mean_aggregator.aggregate(slope_diffs)
        slope_rms = rms_aggregator.aggregate(slope_diffs)

        results = {} 
        results["slope_diffs_mean"] = slope_mean
        results["slope_diffs_rms"] = slope_rms

        return results
