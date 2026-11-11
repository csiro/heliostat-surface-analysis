from typing import Union, Optional, cast, Any, Dict

import os
import numpy as np
from stl.mesh import Mesh

from heliostat_surface_analysis.linear_function.plane import Plane
from heliostat_surface_analysis.linear_function.circular_paraboloid import CircularParaboloid
from heliostat_surface_analysis.linear_function.anu_polynomial import ANUPolynomial
from heliostat_surface_analysis.analyser.analyser import Analyser
from heliostat_surface_analysis.comparitor.comparitor import AngularDifferenceComparitor
from heliostat_surface_analysis.fitter.fitter import LinearLeastSquaresFitter
from heliostat_surface_analysis.mesher.mesher import Mesher
from heliostat_surface_analysis.aggregator.aggregator import MeanAggregator
from heliostat_surface_analysis.aggregator.aggregator import RMSAggregator
from heliostat_surface_analysis.exporter.exporter import export_points_resampled_stl


class FitSurfaceAnalyser(Analyser):
    def __init__(
        self,
        params: Optional[Dict[str, Union[str, float]]]
    ):
        params = cast(Dict[str, Union[str, float]], params)

        if "surface" not in params:
            raise ValueError("FitSurfaceAnalyser requires the 'surface' parameter to be set")

        if params["surface"] == "flat":
            self.reference = Plane()
        elif params["surface"] == "circular_paraboloid":
            self.reference = CircularParaboloid()
        elif params["surface"] == "anu_polynomial":
            self.reference = ANUPolynomial()
        else:
            raise ValueError(f"{params['surface']} is not a valid surface")

    def analyse(
        self,
        x: np.ndarray,
        y: np.ndarray,
        z: np.ndarray,
        mesh: Mesh,
        scan_name: str = ""
    ) -> Dict[str, Any]:
        x_c, y_c, _, areas, normals = Mesher.get_facets(mesh)

        fitter = LinearLeastSquaresFitter()
        coeffs = fitter.fit(self.reference.terms, x, y, z)
        f_n = self.reference.assemble_normal_function(coeffs)
        ideal_normals = f_n(x_c, y_c)

        f = self.reference.assemble_function(coeffs)
        ideal_zs = f(x, y)

        angle_comparitor = AngularDifferenceComparitor()
        slope_errors = angle_comparitor.compare(normals, ideal_normals)

        return areas, normals, coeffs, ideal_normals, ideal_zs, slope_errors

    def get_coefficient_labels(self) -> list:
        return self.reference.get_coefficient_labels()
