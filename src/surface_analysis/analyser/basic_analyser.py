import numpy as np
import pandas as pd

from surface_analysis.measured_surface import MeasuredSurface
from surface_analysis.linear_function.circular_paraboloid import CircularParaboloid
from surface_analysis.linear_function.plane import Plane
from surface_analysis.linear_function.fixed_paraboloid import FixedParaboloid
from surface_analysis.plotter import Plotter
from surface_analysis.fitter.fitter import LinearLeastSquaresFitter
from surface_analysis.measured_surface import MeasuredSurface
from surface_analysis.comparitor.comparitor import DifferenceComparitor
from surface_analysis.comparitor.comparitor import AngularDifferenceComparitor
from surface_analysis.aggregator.aggregator import WeightedRMSAggregator


class BasicAnalyser:
    def analyse(
        self,
        surface: MeasuredSurface,
        scan_name: str,
        output_dir: str,
        design_focal_length: float,
    ) -> pd.DataFrame:
        results = {}
        results["name"] = scan_name
        results["design_focal_length"] = design_focal_length

        plotter = Plotter()
        plotter.plot_points(surface.x, surface.y, surface.z, output_dir, "raw")
        plotter.plot_points_as_surface(surface.x, surface.y, surface.z, surface.z_c, output_dir, "raw")
        plotter.plot_points_2d(surface.x, surface.y, surface.z_c, output_dir, "raw")

        poly = CircularParaboloid()
        fitter = LinearLeastSquaresFitter()

        coeffs = fitter.fit(poly.terms, surface.x, surface.y, surface.z)
        results["fit_focal_length"] = 1 / (4 * coeffs[0, 0])

        f = poly.assemble_function(coeffs)
        z = f(surface.x, surface.y)
        z_c = f(surface.x_c, surface.y_c)

        diff_comparitor = DifferenceComparitor()
        z_diffs = diff_comparitor.compare(z, surface.z)
        z_c_diffs = diff_comparitor.compare(z_c, surface.z_c)
        plotter.plot_points(surface.x, surface.y, z_diffs, output_dir, "circular_paraboloid_z_diffs")
        plotter.plot_points_as_surface(surface.x, surface.y, z_diffs, z_c_diffs, output_dir, "circular_paraboloid_z_diffs2", True)
        plotter.plot_points_2d(surface.x, surface.y, z_c_diffs, output_dir, "circular_paraboloid_z_diffs", True)

        f_n = poly.assemble_normal_function(coeffs)
        n = f_n(surface.x_c, surface.y_c)

        angle_comparitor = AngularDifferenceComparitor()
        slope_diffs = angle_comparitor.compare(n, surface.n)
        plotter.plot_points(surface.x_c, surface.y_c, slope_diffs, output_dir, "circular_paraboloid_slope_diffs")
        plotter.plot_points_2d(surface.x, surface.y, slope_diffs, output_dir, "circular_paraboloid_slope_diffs")

        aggregator = WeightedRMSAggregator(surface.area)
        slope_rms = aggregator.aggregate(slope_diffs)
        results["circular_paraboloid_slope_diffs_rms"] = slope_rms
        results["circular_paraboloid_mle_sigma"] = slope_rms / np.sqrt(2)

        df_dx = poly.assemble_terms_and_coeffs(poly.df_dx_terms, coeffs)
        df_dy = poly.assemble_terms_and_coeffs(poly.df_dy_terms, coeffs)
        ref_df_dx = df_dx(surface.x_c, surface.y_c)
        ref_df_dy = df_dy(surface.x_c, surface.y_c)
        meas_dz_dx = -surface.n[:, 0] / surface.n[:, 2]
        meas_dz_dy = -surface.n[:, 1] / surface.n[:, 2]
        x_slope_diffs = meas_dz_dx.reshape(-1, 1) - ref_df_dx
        y_slope_diffs = meas_dz_dy.reshape(-1, 1) - ref_df_dy

        plotter.plot_points_2d(surface.x, surface.y, x_slope_diffs, output_dir, "circular_paraboloid_x_slope_diffs", True)
        plotter.plot_points_2d(surface.x, surface.y, y_slope_diffs, output_dir, "circular_paraboloid_y_slope_diffs", True)

        design_a_parameter = 1 / (4 * design_focal_length)
        paraboloid = FixedParaboloid()
        p = paraboloid.assemble_function(np.array([design_a_parameter]))
        p_z = p(surface.x, surface.y)

        plane = Plane()
        plane_coeffs = fitter.fit(plane.terms, surface.x, surface.y, surface.z - p_z.reshape(-1, 1))

        f_n = poly.assemble_normal_function(np.insert(plane_coeffs, 0, design_a_parameter, axis=0))
        n = f_n(surface.x_c, surface.y_c)
        slope_diffs = angle_comparitor.compare(n, surface.n)
        plotter.plot_points_2d(surface.x, surface.y, slope_diffs, output_dir, "fixed_paraboloid_slope_diffs")
        slope_rms = aggregator.aggregate(slope_diffs)

        results["fixed_paraboloid_slope_diffs_rms"] = slope_rms
        results["fixed_paraboloid_mle_sigma"] = slope_rms / np.sqrt(2)

        return results
