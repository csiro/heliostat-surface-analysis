from typing import Union, Optional, cast, Any, Dict

import numpy as np

from surface_analysis.linear_function.plane import Plane
from surface_analysis.linear_function.circular_paraboloid import CircularParaboloid
from surface_analysis.analyzer.analyzer import Analyzer
from surface_analysis.comparitor.comparitor import AngularDifferenceComparitor
from surface_analysis.fitter.fitter import LinearLeastSquaresFitter
from surface_analysis.mesh.default_mesher import DefaultMesher
from surface_analysis.aggregator.aggregator import WeightedRMSAggregator


class KnownFocalAnalyzer(Analyzer):
    def __init__(
        self,
        params: Optional[Dict[str, Union[str, float]]]
    ):
        params = cast(Dict[str, Union[str, float]], params)

        if "focal_length_file" not in params:
            raise ValueError("KnownFocalAnalyzer requires the 'focal_length_file' parameter to be set")
        if "max_edge_length" not in params:
            raise ValueError("KnownFocalAnalyzer requires the 'max_edge_length' parameter to be set")

        self.max_edge_length = float(params["max_edge_length"])
        self.focal_lengths = self.load_design_focal_lengths(str(params["focal_length_file"]))

    def analyze(
        self,
        x: np.ndarray,
        y: np.ndarray,
        z: np.ndarray,
        scan_name: str = "",
    ) -> Dict[str, Any]:
        if scan_name == "":
            raise ValueError(f"Scan name not provided")
        elif scan_name not in self.focal_lengths.keys():
            raise ValueError(f"Scan name {scan_name} not found in focal_length_file")

        mesher = DefaultMesher(self.max_edge_length)
        x_c, y_c, _, area, n = mesher.points_to_facets(x, y, z)

        a_parameter = 1 / (4 * self.focal_lengths[scan_name])
        poly = CircularParaboloid()
        p = poly.assemble_function(np.array([a_parameter, 0, 0, 0]))
        p_z = p(x, y)

        fitter = LinearLeastSquaresFitter()

        plane = Plane()
        plane_coeffs = fitter.fit(plane.terms, x, y, z - p_z.reshape(-1, 1))
        f_n = poly.assemble_normal_function(np.insert(plane_coeffs, 0, a_parameter, axis=0))

        angle_comparitor = AngularDifferenceComparitor()
        aggregator = WeightedRMSAggregator(area)

        slope_diffs = angle_comparitor.compare(n, f_n(x_c, y_c))
        slope_rms = aggregator.aggregate(slope_diffs)

        results = {} 
        results["slope_diffs_weighted_rms"] = slope_rms

        return results

    def load_design_focal_lengths(self, focal_length_filename: str) -> Dict[str, float]:
        focal_lengths = {}
        with open(focal_length_filename, "r") as focal_length_file:
            for line in focal_length_file.readlines():
                parts = line.split()
                scan_name = parts[0]
                design_focal_length = float(parts[1])
                focal_lengths[scan_name] = design_focal_length

        return focal_lengths
