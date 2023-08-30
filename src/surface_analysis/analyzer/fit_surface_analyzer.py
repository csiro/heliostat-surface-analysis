from typing import Union, Optional, cast, Any, Dict

import os
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
from surface_analysis.exporter.exporter import export_points_resampled_stl


class FitSurfaceAnalyzer(Analyzer):
    def __init__(
        self,
        params: Optional[Dict[str, Union[str, float]]],
        output_dir: str
    ):
        params = cast(Dict[str, Union[str, float]], params)

        if "surface" not in params:
            raise ValueError("FitSurfaceAnalyzer requires the 'surface' parameter to be set")
        if "max_edge_length" not in params:
            raise ValueError("FitSurfaceAnalyzer requires the 'max_edge_length' parameter to be set")

        if params["surface"] == "flat":
            self.reference = Plane()
        elif params["surface"] == "circular_paraboloid":
            self.reference = CircularParaboloid()
        elif params["surface"] == "anu_polynomial":
            self.reference = ANUPolynomial()
        else:
            raise ValueError(f"{params['surface']} is not a valid surface")

        self.max_edge_length = float(params["max_edge_length"])
        
        self.output_dir = output_dir
        
        if "write_STLs" in params:        
            self.write_STLs = params["write_STLs"]
        else:
            self.write_STLs = False
            
        if "width" not in params or "height" not in params:
            self.width = None
            self.height = None
        else:
            self.width = float(params["width"])
            self.height = float(params["height"])

    def analyze(
        self,
        x: np.ndarray,
        y: np.ndarray,
        z: np.ndarray,
        scan_name: str = "",
    ) -> Dict[str, Any]:
        mesher = DefaultMesher(self.max_edge_length)
        mesh, x_c, y_c, _, _, n = mesher.points_to_facets(x, y, z)
        if self.write_STLs:
            mesh.save(os.path.join(self.output_dir,f"{scan_name}_raw_delaunay.stl"))
            if self.width!=None and self.height!=None:
             export_points_resampled_stl(x,y,z,self.width,self.height,os.path.join(self.output_dir,f"{scan_name}_raw_resampled.stl"))

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
        results["coeffs"] = coeffs

        return results
