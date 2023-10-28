from typing import Union, Optional, cast, Any, Dict

import os
import numpy as np

from surface_analysis.linear_function.plane import Plane
from surface_analysis.linear_function.circular_paraboloid import CircularParaboloid
from surface_analysis.linear_function.anu_polynomial import ANUPolynomial
from surface_analysis.analyzer.analyzer import Analyzer
from surface_analysis.comparitor.comparitor import AngularDifferenceComparitor
from surface_analysis.fitter.fitter import LinearLeastSquaresFitter
from surface_analysis.mesher.mesher import Mesher
from surface_analysis.aggregator.aggregator import MeanAggregator
from surface_analysis.aggregator.aggregator import RMSAggregator
from surface_analysis.exporter.exporter import export_points_resampled_stl


class FitSurfaceAnalyzer(Analyzer):
    def __init__(
        self,
        params: Optional[Dict[str, Union[str, float]]],
        mesher: Mesher,
        output_dir: str
    ):
        params = cast(Dict[str, Union[str, float]], params)

        if "surface" not in params:
            raise ValueError("FitSurfaceAnalyzer requires the 'surface' parameter to be set")

        if params["surface"] == "flat":
            self.reference = Plane()
        elif params["surface"] == "circular_paraboloid":
            self.reference = CircularParaboloid()
        elif params["surface"] == "anu_polynomial":
            self.reference = ANUPolynomial()
        else:
            raise ValueError(f"{params['surface']} is not a valid surface")
        
        if "write_STLs" in params:        
            self.write_STLs = params["write_STLs"]
        else:
            self.write_STLs = False
        
        self.mesher = mesher
        self.output_dir = output_dir

    def analyze(
        self,
        x: np.ndarray,
        y: np.ndarray,
        z: np.ndarray,
        scan_name: str = "",
    ) -> Dict[str, Any]:
        mesh = self.mesher.create_mesh(x, y, z)
        if self.write_STLs:
            mesh.save(os.path.join(self.output_dir,f"{scan_name}.stl"))
        x_c, y_c, _, areas, normals = Mesher.get_facets(mesh)
        
        fitter = LinearLeastSquaresFitter()
        coeffs = fitter.fit(self.reference.terms, x, y, z)
        f_n = self.reference.assemble_normal_function(coeffs)
        ideal_normals = f_n(x_c, y_c)
        
        angle_comparitor = AngularDifferenceComparitor()
        slope_errors = angle_comparitor.compare(normals, ideal_normals)

        return areas, normals, coeffs, ideal_normals, slope_errors
