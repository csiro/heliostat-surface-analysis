from typing import Union, Optional, cast, Any, Dict

import numpy as np

from surface_analysis.linear_function.plane import Plane
from surface_analysis.linear_function.circular_paraboloid import CircularParaboloid
from surface_analysis.linear_function.anu_polynomial import ANUPolynomial
from surface_analysis.analyzer.analyzer import Analyzer
from surface_analysis.comparitor.comparitor import AngularDifferenceComparitor
from surface_analysis.fitter.fitter import LinearLeastSquaresFitter
from surface_analysis.mesh.default_mesher import DefaultMesher
from surface_analysis.aggregator.aggregator import MeanAggregator
from surface_analysis.aggregator.aggregator import RMSAggregator


class FitCurveAnalyzer(Analyzer):
    def __init__(
        self,
        params: Optional[Dict[str, Union[str, float]]]
    ):
        params = cast(Dict[str, Union[str, float]], params)

        if "curve" not in params:
            raise ValueError("FitCurveAnalyzer requires the 'curve' parameter to be set")
        if "max_edge_length" not in params:
            raise ValueError("FitCurveAnalyzer requires the 'max_edge_length' parameter to be set")

        if params["curve"] == "flat":
            self.reference = Plane()
        elif params["curve"] == "circular_paraboloid":
            self.reference = CircularParaboloid()
        elif params["curve"] == "anu_polynomial":
            self.reference = ANUPolynomial()
        else:
            raise ValueError(f"{params['curve']} is not a valid curve")

        self.max_edge_length = float(params["max_edge_length"])

    def analyze(
        self,
        x: np.ndarray,
        y: np.ndarray,
        z: np.ndarray,
        scan_name: str = "",
    ) -> Dict[str, Any]:
        mesher = DefaultMesher(self.max_edge_length)
        x_c, y_c, _, _, n = mesher.points_to_facets(x, y, z)

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
