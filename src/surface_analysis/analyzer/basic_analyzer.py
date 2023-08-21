from typing import Any

import numpy as np
import pandas as pd

from surface_analysis.analyzer.analyzer import Analyzer
from surface_analysis.old.measured_surface import MeasuredSurface
from surface_analysis.linear_function.circular_paraboloid import CircularParaboloid
from surface_analysis.linear_function.plane import Plane
from surface_analysis.linear_function.fixed_paraboloid import FixedParaboloid
from surface_analysis.mesh.default_mesher import DefaultMesher
from surface_analysis.plotter import Plotter
from surface_analysis.fitter.fitter import LinearLeastSquaresFitter
from surface_analysis.old.measured_surface import MeasuredSurface
from surface_analysis.comparitor.comparitor import DifferenceComparitor
from surface_analysis.comparitor.comparitor import AngularDifferenceComparitor
from surface_analysis.aggregator.aggregator import WeightedRMSAggregator


class BasicAnalyzer(Analyzer):
    def __init__(self, scan_names, design_focal_lengths, output_dir):
        self.scan_names = scan_names
        self.design_focal_length = design_focal_lengths
        self.output_dir = output_dir

    def analyze(
        self,
        x: np.ndarray,
        y: np.ndarray,
        z: np.ndarray,
    ) -> pd.DataFrame:
        results = {}
        results["name"] = self.scan_name
        results["design_focal_length"] = self.design_focal_length

        mesher = DefaultMesher(self.max_edge_length)
        x_c, y_c, z_c, area, n = mesher.points_to_facets(x, y, z)

        plotter = Plotter()
        plotter.plot_points(x, y, z, self.output_dir, "raw", "m", "m", "m")
        plotter.plot_points_as_surface(x, y, z, z_c, self.output_dir, "raw", "m", "m", "m")
        plotter.plot_points_2d(x, y, z_c, self.output_dir, "raw", "m", "m", "m")

        poly = CircularParaboloid()
        fitter = LinearLeastSquaresFitter()

        coeffs = fitter.fit(poly.terms, x, y, z)
        results["fit_focal_length"] = 1 / (4 * coeffs[0, 0])

        f = poly.assemble_function(coeffs)
        z = f(x, y)
        z_c = f(x_c, y_c)

        diff_comparitor = DifferenceComparitor()
        z_diffs = diff_comparitor.compare(z, z)
        z_c_diffs = diff_comparitor.compare(z_c, z_c)
        plotter.plot_points(x, y, z_diffs, self.output_dir, "circular_paraboloid_z_diffs", "m", "m", "m")
        plotter.plot_points_as_surface(x, y, z_diffs, z_c_diffs, self.output_dir, "circular_paraboloid_z_diffs2", "m", "m", "m", zero=True)
        plotter.plot_points_2d(x, y, z_c_diffs, self.output_dir, "circular_paraboloid_z_diffs", "m", "m", "m", zero=True)

        f_n = poly.assemble_normal_function(coeffs)
        n = f_n(x_c, y_c)

        angle_comparitor = AngularDifferenceComparitor()
        slope_diffs = angle_comparitor.compare(n, n)
        plotter.plot_points(x_c, y_c, slope_diffs, self.output_dir, "circular_paraboloid_slope_diffs", "m", "m", "rad")
        plotter.plot_points_2d(x, y, slope_diffs, self.output_dir, "circular_paraboloid_slope_diffs", "m", "m", "rad")

        aggregator = WeightedRMSAggregator(area)
        slope_rms = aggregator.aggregate(slope_diffs)
        results["circular_paraboloid_slope_diffs_rms"] = slope_rms
        results["circular_paraboloid_mle_sigma"] = slope_rms / np.sqrt(2)

        df_dx = poly.assemble_terms_and_coeffs(poly.df_dx_terms, coeffs)
        df_dy = poly.assemble_terms_and_coeffs(poly.df_dy_terms, coeffs)
        ref_df_dx = df_dx(x_c, y_c)
        ref_df_dy = df_dy(x_c, y_c)
        meas_dz_dx = -n[:, 0] / n[:, 2]
        meas_dz_dy = -n[:, 1] / n[:, 2]
        x_slope_diffs = meas_dz_dx.reshape(-1, 1) - ref_df_dx
        y_slope_diffs = meas_dz_dy.reshape(-1, 1) - ref_df_dy

        plotter.plot_points_2d(x, y, x_slope_diffs, self.output_dir, "circular_paraboloid_x_slope_diffs", "m", "m", "gradient", True)
        plotter.plot_points_2d(x, y, y_slope_diffs, self.output_dir, "circular_paraboloid_y_slope_diffs", "m", "m", "gradient", True)

        design_a_parameter = 1 / (4 * self.design_focal_length)
        paraboloid = FixedParaboloid()
        p = paraboloid.assemble_function(np.array([design_a_parameter]))
        p_z = p(x, y)

        plane = Plane()
        plane_coeffs = fitter.fit(plane.terms, x, y, z - p_z.reshape(-1, 1))

        f_n = poly.assemble_normal_function(np.insert(plane_coeffs, 0, design_a_parameter, axis=0))
        n = f_n(x_c, y_c)
        slope_diffs = angle_comparitor.compare(n, n)
        plotter.plot_points_2d(x, y, slope_diffs, self.output_dir, "fixed_paraboloid_slope_diffs", "m", "m", "rad")
        slope_rms = aggregator.aggregate(slope_diffs)

        results["fixed_paraboloid_slope_diffs_rms"] = slope_rms
        results["fixed_paraboloid_mle_sigma"] = slope_rms / np.sqrt(2)

        return results
