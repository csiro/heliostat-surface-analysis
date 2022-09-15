import os

import numpy as np
from scipy import stats
from matplotlib import pyplot as plt
import nlopt

from surface_analysis.loader import Loader
from surface_analysis.cleaner import Cleaner
from surface_analysis.linear_functions.linear_function_creator import (
    LinearFunctionCreator,
)
from surface_analysis.linear_functions.linear_function_assembler import (
    LinearFunctionAssembler,
)
from surface_analysis.linear_least_squares_fitter import LinearLeastSquaresFitter
from surface_analysis.linear_objective_functions import (
    mean_slope_error_objective,
    squared_z_distance_objective,
)
from surface_analysis.plotter import Plotter
from surface_analysis.points_to_mesh_converter import PointsToMeshConverter
from surface_analysis.slope_error import SlopeErrorCalculator


def main():
    file_name = r"C:\Users\ACU005\CSIRO\ASTRI P11 Heliostats - HelioCon\HeliostatMetrology\HelioJigScans\surface_D.txt"
    mirror_name_with_extension = os.path.basename(os.path.normpath(file_name))
    mirror_name = mirror_name_with_extension.split(".")[0]
    output_dir = os.path.join("outputs", mirror_name)
    os.makedirs(output_dir, exist_ok=True)

    # anu_method(file_name, output_dir)
    csiro_method(file_name, output_dir)


def csiro_method(file_name, output_dir):
    loader = Loader()
    raw_x, raw_y, raw_z = loader.from_leica(file_name)

    cleaner = Cleaner()
    centred_x, centred_y, centred_z = cleaner.centre_points_centroid(
        raw_x, raw_y, raw_z
    )
    x, y, z = cleaner.rotate_points_PCA(centred_x, centred_y, centred_z)

    lfc = LinearFunctionCreator()
    poly = lfc.circular_paraboloid()

    p2m = PointsToMeshConverter()
    x_c, y_c, z_c, area, n = p2m.points_to_normals(x, y, z)

    obj = squared_z_distance_objective(x, y, z, poly)
    opt = nlopt.opt(nlopt.LN_COBYLA, 4)
    opt.set_lower_bounds([-1, -1, -1, -1])
    opt.set_upper_bounds([1, 1, 1, 1])
    opt.set_min_objective(obj)
    opt.set_xtol_rel(1e-6)
    xopt = opt.optimize([0, 0, 0, 0])
    minf = opt.last_optimum_value()
    print(f"optimum at {xopt[0]}, {xopt[1]}, {xopt[2]} {xopt[3]}\n")
    print(f"minimum value = {minf}\n")
    print(f"result code = {opt.last_optimize_result()}\n")
    print("\n")

    obj = mean_slope_error_objective(x_c, y_c, n, area, poly)
    opt = nlopt.opt(nlopt.LN_COBYLA, 4)
    opt.set_lower_bounds([-1, -1, -1, -1])
    opt.set_upper_bounds([1, 1, 1, 1])
    opt.set_min_objective(obj)
    opt.set_xtol_rel(1e-6)
    xopt = opt.optimize([0, 0, 0, 0])
    minf = opt.last_optimum_value()
    print(f"optimum at {xopt[0]}, {xopt[1]}, {xopt[2]} {xopt[3]}\n")
    print(f"minimum value = {minf}\n")
    print(f"result code = {opt.last_optimize_result()}\n")

    exit()

    with open(os.path.join(output_dir, "nlopt_results.txt"), "w") as file:
        file.write("Doing nlopt for OLS of circular paraboloid\n")
        obj = ordinary_least_squares_objective(x, y, z)
        opt = nlopt.opt(nlopt.LN_COBYLA, 4)
        opt.set_lower_bounds([-1, -1, -1, -1])
        opt.set_upper_bounds([1, 1, 1, 1])
        opt.set_min_objective(obj)
        opt.set_xtol_rel(1e-6)
        xopt = opt.optimize([0, 0, 0, 0])
        minf = opt.last_optimum_value()
        file.write(f"optimum at {xopt[0]}, {xopt[1]}, {xopt[2]} {xopt[3]}\n")
        file.write(f"minimum value = {minf}\n")
        file.write(f"result code = {opt.last_optimize_result()}\n")
        file.write("\n")

        file.write("Doing nlopt for min mean slope error of circular paraboloid\n")
        p2m = PointsToMeshConverter()
        x_c, y_c, z_c, area, n = p2m.points_to_normals(x, y, z)
        obj = min_mean_slope_error_objective(x_c, y_c, n, area)
        opt = nlopt.opt(nlopt.LN_COBYLA, 4)
        opt.set_lower_bounds([-1, -1, -1, -1])
        opt.set_upper_bounds([1, 1, 1, 1])
        opt.set_min_objective(obj)
        opt.set_xtol_rel(1e-6)
        xopt = opt.optimize([0, 0, 0, 0])
        minf = opt.last_optimum_value()
        file.write(f"optimum at {xopt[0]}, {xopt[1]}, {xopt[2]} {xopt[3]}\n")
        file.write(f"minimum value = {minf}\n")
        file.write(f"result code = {opt.last_optimize_result()}\n")


def anu_method(file_name, output_dir):
    loader = Loader()
    raw_x, raw_y, raw_z = loader.from_leica(file_name)

    cleaner = Cleaner()
    centred_x, centred_y, centred_z = cleaner.centre_points_centroid(
        raw_x, raw_y, raw_z
    )
    x, y, z = cleaner.rotate_points_PCA(centred_x, centred_y, centred_z)

    plotter = Plotter()
    plotter.initial_verification_plots(x, y, z, output_dir)

    lfc = LinearFunctionCreator()
    polynomials = [
        lfc.centred_circular_paraboloid(),
        lfc.centred_circular_paraboloid_with_z_offset(),
        lfc.circular_paraboloid(),
        lfc.elliptic_paraboloid(),
        lfc.general_paraboloid(),
        lfc.high_order_poly(),
    ]

    decimals = 6
    fitter = LinearLeastSquaresFitter()
    assembler = LinearFunctionAssembler()
    sec = SlopeErrorCalculator()
    with open(os.path.join(output_dir, "fit_results.txt"), "w") as file:
        for poly in polynomials:
            coeffs, ssr = fitter.fit_linear_function(x, y, z, poly.terms)
            file.write(f"Fit for {poly.name}\n")
            file.write(f"Formula: {poly.formula}\n")
            file.write(
                f"Coefficients: {[round(coeff[0], decimals) for coeff in coeffs]}\n"
            )
            file.write(f"Sum of Squared Residuals (z-value): {round(ssr, decimals)}\n")
            file.write(
                f"RMS of Residuals (z-value): {round(np.sqrt(ssr / len(x)), decimals)}\n"
            )

            f = assembler.assemble_linear_function(poly.terms, coeffs)
            normal_func = assembler.assemble_normal_function(
                poly.df_dx_terms, poly.df_dy_terms, coeffs
            )

            z_fit = f(x, y)
            residual = z - z_fit
            plotter.fit_verification_plots(x, y, z_fit, output_dir, poly.name)
            plotter.fit_verification_plots(
                x, y, residual, output_dir, f"{poly.name}_residual"
            )

            p2m = PointsToMeshConverter()
            x_c, y_c, z_c, area, n = p2m.points_to_normals(x, y, z)
            angular_differences = sec.calculate_angular_differences(
                x_c, y_c, n, normal_func
            )

            count = len(angular_differences)
            cutoff = round(count * 99 / 100)
            combined = np.hstack([angular_differences, area])
            ordered = combined[combined[:, 0].argsort()]
            angular_differences_trunc = ordered[:, 0][:cutoff]
            area_trunc = ordered[:, 1][:cutoff]

            file.write("Slope Error Calculations:\n")
            weighted_mean = sec.calculate_weighted_mean(angular_differences, area)
            sigma_mean = weighted_mean / np.sqrt(np.pi / 2)
            file.write(
                f"Weighted Mean:{round(weighted_mean, decimals)} gives sigma:{round(sigma_mean, decimals)}\n"
            )
            weighted_rms = sec.calculate_weighted_rms(angular_differences, area)
            sigma_mle = weighted_rms / np.sqrt(2)
            file.write(
                f"Area weighted RMS:{round(weighted_rms, decimals)} gives MLE (neglecting correction factor):{round(sigma_mle, decimals)}\n"
            )

            file.write("Slope Error Calculations Missing top 1 percent of data:\n")
            weighted_mean_trunc = sec.calculate_weighted_mean(
                angular_differences_trunc, area_trunc
            )
            sigma_mean_trunc = weighted_mean_trunc / np.sqrt(np.pi / 2)
            file.write(
                f"Weighted Mean:{round(weighted_mean_trunc, decimals)} gives sigma:{round(sigma_mean_trunc, decimals)}\n"
            )
            weighted_rms_trunc = sec.calculate_weighted_rms(
                angular_differences_trunc, area_trunc
            )
            sigma_mle_trunc = weighted_rms_trunc / np.sqrt(2)
            file.write(
                f"Area weighted RMS:{round(weighted_rms_trunc, decimals)} gives MLE (neglecting correction factor):{round(sigma_mle_trunc, decimals)}\n"
            )

            bins = 100
            plotter.slope_verification_plots(
                angular_differences, output_dir, poly.name, bins
            )
            plotter.slope_verification_plots(
                angular_differences_trunc, output_dir, f"{poly.name}_trunc", bins
            )

            rvs = angular_differences.reshape((-1,))
            plt.clf()
            stats.probplot(rvs, dist=stats.rayleigh, plot=plt, rvalue=True)
            plt.savefig(os.path.join(output_dir, f"{poly.name}_qq_plot"))

            rvs = angular_differences_trunc.reshape((-1,))
            plt.clf()
            stats.probplot(rvs, dist=stats.rayleigh, plot=plt, rvalue=True)
            plt.savefig(os.path.join(output_dir, f"{poly.name}_trunc_qq_plot"))

            file.write(f"\n")


if __name__ == "__main__":
    main()
