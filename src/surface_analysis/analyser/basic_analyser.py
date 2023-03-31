import numpy as np
import pandas as pd

from surface_analysis.measured_surface import MeasuredSurface
from surface_analysis.linear_function.circular_paraboloid import CircularParaboloid
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
        plotter.plot_points_as_surface(surface.x, surface.y, surface.z, output_dir, "raw")
        plotter.plot_points_2d(surface.x, surface.y, surface.z, output_dir, "raw")

        poly = CircularParaboloid()
        fitter = LinearLeastSquaresFitter()

        coeffs = fitter.fit(poly.terms, surface.x, surface.y, surface.z)
        results[f"fit_focal_length"] = 1 / (4 * coeffs[0, 0])

        f = poly.assemble_function(coeffs)
        z = f(surface.x, surface.y)

        diff_comparitor = DifferenceComparitor()
        z_diffs = diff_comparitor.compare(z, surface.z)
        plotter.plot_points(surface.x, surface.y, z_diffs, output_dir, "circular_paraboloid_z_diffs")
        plotter.plot_points_as_surface(surface.x, surface.y, z_diffs, output_dir, "circular_paraboloid_z_diffs")
        plotter.plot_points_2d(surface.x, surface.y, z_diffs, output_dir, "circular_paraboloid_z_diffs")

        f_n = poly.assemble_normal_function(coeffs)
        n = f_n(surface.x_c, surface.y_c)

        angle_comparitor = AngularDifferenceComparitor()
        slope_diffs = angle_comparitor.compare(n, surface.n)    
        plotter.plot_points(surface.x_c, surface.y_c, slope_diffs, output_dir, "circular_paraboloid_slope_diffs")
        plotter.plot_points_as_surface(surface.x_c, surface.y_c, slope_diffs, output_dir, "circular_paraboloid_slope_diffs")
        plotter.plot_points_2d(surface.x_c, surface.y_c, slope_diffs, output_dir, "circular_paraboloid_slope_diffs")

        aggregator = WeightedRMSAggregator(surface.area)
        slope_rms = aggregator.aggregate(slope_diffs)
        results["circular_paraboloid_slope_diffs_rms"] = slope_rms
        results["circular_paraboloid_mle_sigma"] = slope_rms / np.sqrt(2)

        return results
