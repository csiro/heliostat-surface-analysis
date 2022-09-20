import os
from typing import Any

import numpy as np
import pandas as pd

from surface_analysis.loaders.default_loader import DefaultLoader
from surface_analysis.loaders.leica_loader import LeicaLoader
from surface_analysis.preprocessor import Preprocessor
from surface_analysis.preprocessor import BasicPreprocessor
from surface_analysis.linear_functions.linear_function import LinearFunction
from surface_analysis.linear_functions.circular_paraboloid import CircularParaboloid
from surface_analysis.linear_functions.anu_polynomial import ANUPolynomial
from surface_analysis.fitter import LinearLeastSquaresFitter
from surface_analysis.fitter import NonLinearFitter
from surface_analysis.linear_objective_function import SlopeErrorObjectiveFunction
from surface_analysis.measured_surface import MeasuredSurface
from surface_analysis.points_to_mesh_converter import points_to_normals
from surface_analysis.exporter import export_points_delaunay_stl
from surface_analysis.exporter import export_points_resampled_stl
from surface_analysis.exporter import export_function_stl


MANIFEST_FILE = "designfocallengths.txt"
SCANS_DIR = "scans"
WIDTH = 2.25
HEIGHT = 2.25


def analyse_scans(
    input_path: str,
    output_path: str
):
    manifest_path = os.path.join(input_path, MANIFEST_FILE)
    focal_lengths = load_focal_lengths(manifest_path)

    # loader = DefaultLoader()
    loader = LeicaLoader()
    scan_dir_path = os.path.join(input_path, SCANS_DIR)
    scan_file_names = os.listdir(scan_dir_path)
    analysis_results = []
    for scan_file_name in scan_file_names:
        scan_path = os.path.join(scan_dir_path, scan_file_name)
        scan_name = scan_file_name.split(".")[0]
        scan_output_dir = os.path.join(output_path, scan_name)
        os.makedirs(scan_output_dir, exist_ok=True)

        x, y, z = loader.load_points(scan_path)
        analysis_result = analyse_scan(
            x,
            y,
            z,
            scan_name,
            scan_output_dir,
            WIDTH,
            HEIGHT,
            focal_lengths[scan_name],
            BasicPreprocessor(),
        )
        analysis_results.append(analysis_result)

    output_table = pd.concat(analysis_results)
    output_table_path = os.path.join(output_path, f"outputs.pkl")
    output_table.to_pickle(output_table_path)


def load_focal_lengths(manifest_path: str) -> dict[str, float]:
    focal_lengths = {}
    with open(manifest_path, "r") as manifest_file:
        for line in manifest_file.readlines():
            parts = line.split("\t")
            scan_name = parts[0]
            design_focal_length = float(parts[1])
            focal_lengths[scan_name] = design_focal_length
    return focal_lengths


def analyse_scan(
    raw_x: np.ndarray,
    raw_y: np.ndarray,
    raw_z: np.ndarray,
    scan_name: str,
    scan_output_dir: str,
    width: float,
    height: float,
    design_focal_length: float,
    preprocessor: Preprocessor,
) -> pd.DataFrame:
    x, y, z = preprocessor.preprocess_points(raw_x, raw_y, raw_z)
    x_c, y_c, z_c, area, n = points_to_normals(x, y, z)
    surface = MeasuredSurface(x, y, z, x_c, y_c, z_c, n, area)


    results = {}
    results["name"] = scan_name
    results["width"] = width
    results["height"] = height
    results["design_focal_length"] = design_focal_length

    export_points_delaunay_stl(
        surface.x,
        surface.y,
        surface.z,
        os.path.join(scan_output_dir, f"{scan_name}_raw_delaunay.stl")
    )
    export_points_resampled_stl(
        surface.x,
        surface.y,
        surface.z,
        width,
        height,
        os.path.join(scan_output_dir, f"{scan_name}_raw_resampled.stl")
    )

    poly = CircularParaboloid()
    fitter = LinearLeastSquaresFitter(poly.terms)
    coeffs = fitter.fit(surface.x, surface.y, surface.z)
    analyse_polynomial(
        results,
        "circular_paraboloid_sum_squared_z_diff",
        surface,
        poly,
        coeffs,
        scan_output_dir,
        scan_name,
        width,
        height,
    )

    poly = ANUPolynomial()
    fitter = LinearLeastSquaresFitter(poly.terms)
    coeffs = fitter.fit(surface.x, surface.y, surface.z)
    analyse_polynomial(
        results,
        "anu_polynomial_sum_squared_z_diff",
        surface,
        poly,
        coeffs,
        scan_output_dir,
        scan_name,
        width,
        height,
    )

    poly = CircularParaboloid()
    fitter = NonLinearFitter(
        4,
        SlopeErrorObjectiveFunction(surface.x_c, surface.y_c, surface.n, surface.area, poly),
        [-1, -1, -1, -1],
        [1, 1, 1, 1],
        [0, 0, 0, 0]
    )
    coeffs = fitter.fit()
    analyse_polynomial(
        results,
        "circular_paraboloid_rms_angular_diff",
        surface,
        poly,
        coeffs,
        scan_output_dir,
        scan_name,
        width,
        height,
    )

    output = pd.DataFrame(columns=results.keys())
    for key, value in results.items():
        output.at[0, key] = value
    return output


def analyse_polynomial(
    results: dict[str, Any],
    method_name: str,
    surface: MeasuredSurface,
    poly: LinearFunction,
    coeffs: np.ndarray,
    output_dir: str,
    file_name: str,
    width: float,
    height: float,
):
    obj = SlopeErrorObjectiveFunction(surface.x_c, surface.y_c, surface.n, surface.area, poly)
    weighted_rms = obj.evaluate(coeffs, None)
    sigma_mle = weighted_rms / np.sqrt(2)

    results[f"{method_name}_coeffs"] = coeffs.reshape((-1,))
    results[f"{method_name}_focal_length"] = 1 / (4 * coeffs[0, 0])
    results[f"{method_name}_weighted_rms"] = weighted_rms
    results[f"{method_name}_mle_sigma"] = sigma_mle

    export_function_stl(
        surface.x,
        surface.y,
        poly.assemble_function(coeffs),
        width,
        height,
        os.path.join(output_dir, f"{file_name}_{method_name}.stl")
    )
