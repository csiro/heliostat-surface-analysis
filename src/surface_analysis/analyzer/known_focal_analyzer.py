import os

from typing import Union, Optional, cast, Any, Dict

import numpy as np

from surface_analysis.linear_function.plane import Plane
from surface_analysis.linear_function.circular_paraboloid import CircularParaboloid
from surface_analysis.analyzer.analyzer import Analyzer
from surface_analysis.comparitor.comparitor import AngularDifferenceComparitor
from surface_analysis.fitter.fitter import LinearLeastSquaresFitter
from surface_analysis.mesher.mesher import Mesher
from surface_analysis.aggregator.aggregator import WeightedRMSAggregator
from surface_analysis.exporter.exporter import export_points_resampled_stl

class FocalLength:
    def __init__(self):
        pass
    def get(self,scan_name):
        pass
    
class FixedFocalLength(FocalLength):
    def __init__(self,f):
        self.f = f
    def get(self,scan_name):
        return self.f
    
class PerScanFocalLength(FocalLength):
    def __init__(self,focal_lengths):
        self.focal_lengths = focal_lengths
    def get(self,scan_name):
        if scan_name not in self.focal_lengths.keys():
            raise ValueError(f"Scan name {scan_name} not found in focal_length_file")
        return self.focal_lengths[scan_name]

class KnownFocalAnalyzer(Analyzer):
    def __init__(
        self,
        params: Optional[Dict[str, Union[str, float]]],
        mesher: Mesher,
        output_dir: str
    ):
        params = cast(Dict[str, Union[str, float]], params)
        
        if "focal_length" in params:
            self.focal_length_model = FixedFocalLength(float(params["focal_length"]))
        elif "focal_length_file" in params:
            self.focal_length_model = PerScanFocalLength(self.load_design_focal_lengths(str(params["focal_length_file"])))
        else:
            raise ValueError("KnownFocalAnalyzer requires the 'focal_length_file' or 'focal_length' parameter to be set")
        
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
        if scan_name == "":
            raise ValueError(f"Scan name not provided")
        
        focal_length = self.focal_length_model.get(scan_name)
        
        mesh = self.create_mesh(x, y, z)
        if self.write_STLs:
            mesh.save(os.path.join(self.output_dir,f"{scan_name}.stl"))
        x_c, y_c, _, areas, normals = Mesher.get_facets(mesh)

        a_parameter = 1 / (4 * focal_length)
        poly = CircularParaboloid()
        p = poly.assemble_function(np.array([a_parameter, 0, 0, 0]))
        p_z = p(x, y)

        fitter = LinearLeastSquaresFitter()

        plane = Plane()
        plane_coeffs = fitter.fit(plane.terms, x, y, z - p_z.reshape(-1, 1))
        f_n = poly.assemble_normal_function(np.insert(plane_coeffs, 0, a_parameter, axis=0))
        ideal_normals = f_n(x_c, y_c)

        angle_comparitor = AngularDifferenceComparitor()
        slope_errors = angle_comparitor.compare(normals, ideal_normals)

        return areas, normals, plane_coeffs, ideal_normals, slope_errors

    def load_design_focal_lengths(self, focal_length_filename: str) -> Dict[str, float]:
        focal_lengths = {}
        with open(focal_length_filename, "r") as focal_length_file:
            for line in focal_length_file.readlines():
                parts = line.split()
                scan_name = parts[0]
                design_focal_length = float(parts[1])
                focal_lengths[scan_name] = design_focal_length

        return focal_lengths
