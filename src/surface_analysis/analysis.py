import os
from typing import Any

import numpy as np
import pandas as pd

from surface_analysis.loaders.loader import Loader
from surface_analysis.loaders.default_loader import DefaultLoader
from surface_analysis.preprocessors.preprocessor import Preprocessor
from surface_analysis.preprocessors.basic_preprocessor import BasicPreprocessor
from surface_analysis.linear_functions.linear_function import LinearFunction
from surface_analysis.linear_functions.circular_paraboloid import CircularParaboloid
from surface_analysis.linear_functions.anu_polynomial import ANUPolynomial
from surface_analysis.fitters.fitter import LinearLeastSquaresFitter
from surface_analysis.fitters.fitter import NonLinearFitter
from surface_analysis.objectives.linear_objective_function import SlopeErrorObjectiveFunction
from surface_analysis.measured_surface import MeasuredSurface
from surface_analysis.points_to_mesh_converter import points_to_normals
from surface_analysis.exporters.exporter import export_points_delaunay_stl
from surface_analysis.exporters.exporter import export_points_resampled_stl
from surface_analysis.exporters.exporter import export_function_stl
from surface_analysis.plotter import Plotter
from surface_analysis.comparitors.comparitor import AngularDifferenceComparitor
from surface_analysis.aggregators.aggregator import WeightedRMSAggregator, WeightedMeanAggregator


MANIFEST_FILE = "designfocallengths.txt"
SCANS_DIR = "scans"
WIDTH = 2.25
HEIGHT = 2.25


def analyse_scans(
    input_path: str = "input",
    output_path: str = "output",
    loader: Loader = DefaultLoader,
    preprocessor: Preprocessor = BasicPreprocessor,
):
    design_focal_lengths = load_design_focal_lengths(input_path)

    scans_path = os.path.join(input_path, SCANS_DIR)
    scan_files = os.listdir(scans_path)
    analysis_results = []
    for scan_file in scan_files:
        scan_path = os.path.join(scans_path, scan_file)
        scan_name = scan_file.split(".")[0]
        scan_output_dir = os.path.join(output_path, scan_name)
        os.makedirs(scan_output_dir, exist_ok=True)

        surface = load_measured_surface(scan_path, loader, preprocessor)

        # plotter = Plotter()
        # plotter.plot_points_as_surface(surface.x, surface.y, surface.z)
        # plotter.plot_points(surface.x, surface.y, surface.z)
        # plotter.plot_points_top_view(surface.x, surface.y)

        analysis_result = analyse_scan(
            surface,
            scan_name,
            scan_output_dir,
            WIDTH,
            HEIGHT,
            design_focal_lengths[scan_name],
        )

        output = pd.DataFrame(columns=analysis_result.keys())
        for key, value in analysis_result.items():
            output.at[0, key] = value
        analysis_results.append(output)

    output_table = pd.concat(analysis_results)
    output_table_path = os.path.join(output_path, f"outputs.pkl")
    output_table.to_pickle(output_table_path)


def load_design_focal_lengths(input_path: str) -> dict[str, float]:
    manifest_path = os.path.join(input_path, MANIFEST_FILE)

    focal_lengths = {}
    with open(manifest_path, "r") as manifest_file:
        for line in manifest_file.readlines():
            parts = line.split("\t")
            scan_name = parts[0]
            design_focal_length = float(parts[1])
            focal_lengths[scan_name] = design_focal_length
    return focal_lengths


def load_measured_surface(
    scan_path: str,
    loader: Loader = DefaultLoader,
    preprocessor: Preprocessor = BasicPreprocessor,
) -> MeasuredSurface:
    raw_x, raw_y, raw_z = loader.load_points(scan_path)
    x, y, z = preprocessor.preprocess_points(raw_x, raw_y, raw_z)
    x_c, y_c, z_c, area, n = points_to_normals(x, y, z)
    return MeasuredSurface(x, y, z, x_c, y_c, z_c, n, area)


def analyse_scan(
    surface: MeasuredSurface,
    scan_name: str,
    scan_output_dir: str,
    width: float,
    height: float,
    design_focal_length: float,
) -> pd.DataFrame:
    results = {}
    results["name"] = scan_name
    results["width"] = width
    results["height"] = height
    results["design_focal_length"] = design_focal_length

    export_raw_surface(surface, scan_name, scan_output_dir, width, height)

    # plotter = Plotter()

    # poly1 = CircularParaboloid()
    poly2 = ANUPolynomial()
    # fitter1 = LinearLeastSquaresFitter(poly1.terms)
    fitter2 = LinearLeastSquaresFitter(poly2.terms)
    # coeffs1 = fitter1.fit(surface.x, surface.y, surface.z)
    coeffs2 = fitter2.fit(surface.x, surface.y, surface.z)
    # f1 = poly1.assemble_normal_function(coeffs1)
    f2 = poly2.assemble_normal_function(coeffs2)

    # n1 = f1(surface.x_c, surface.y_c)
    n2 = f2(surface.x_c, surface.y_c)
    # del1 = AngularDifferenceComparitor().compare(n1, surface.n)
    del2 = AngularDifferenceComparitor().compare(n2, surface.n)
    # print(WeightedRMSAggregator(surface.area).aggregate(del1))
    print(WeightedRMSAggregator(surface.area).aggregate(del2))
    print(WeightedMeanAggregator(surface.area).aggregate(del2))
    # del1.sort(axis=0)
    # del2.sort(axis=0)
    # count1 = len(del1)
    # count2 = len(del2)
    # del1 = del1[0: round(count1 * 99 / 100)]
    # del2 = del2[0: round(count2 * 99 / 100)]
    # plotter.plot_hist(del1)
    # plotter.plot_hist(del2)

    # min1 = min(surface.z - f1(surface.x, surface.y))
    # min2 = min(surface.z - f2(surface.x, surface.y))
    # max1 = max(surface.z - f1(surface.x, surface.y))
    # max2 = max(surface.z - f2(surface.x, surface.y))
    # mini = min(min1, min2)
    # maxi = max(max1, max2)

    # plotter.z_lim = (mini, maxi)
    # plotter.plot_points_as_surface_pair(
    #     surface.x,
    #     surface.y,
    #     surface.z - f1(surface.x, surface.y),
    #     surface.z - f2(surface.x, surface.y),
    # )

    # analyse_polynomial(
    #     results,
    #     "circular_paraboloid_sum_squared_z_diff",
    #     surface,
    #     poly1,
    #     coeffs1,
    #     scan_output_dir,
    #     scan_name,
    #     width,
    #     height,
    # )

    analyse_polynomial(
        results,
        "anu_polynomial_sum_squared_z_diff",
        surface,
        poly2,
        coeffs2,
        scan_output_dir,
        scan_name,
        width,
        height,
    )

    # poly = CircularParaboloid()
    # fitter = NonLinearFitter(
    #     4,
    #     SlopeErrorObjectiveFunction(surface.x_c, surface.y_c, surface.n, surface.area, poly),
    #     [-1, -1, -1, -1],
    #     [1, 1, 1, 1],
    #     [0, 0, 0, 0]
    # )
    # coeffs = fitter.fit()
    # analyse_polynomial(
    #     results,
    #     "circular_paraboloid_rms_angular_diff",
    #     surface,
    #     poly,
    #     coeffs,
    #     scan_output_dir,
    #     scan_name,
    #     width,
    #     height,
    # )

    return results


def export_raw_surface(
    surface: MeasuredSurface,
    scan_name: str,
    scan_output_dir: str,
    width: float,
    height: float,
) -> None:
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
