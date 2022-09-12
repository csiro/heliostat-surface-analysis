import numpy as np
from scipy import stats

from surface_analysis.gradient_terms import GradientTerms
from surface_analysis.linear_function_assembler import LinearFunctionAssembler
from surface_analysis.linear_least_squares_fitter import LinearLeastSquaresFitter
from surface_analysis.linear_terms import LinearTerms
from surface_analysis.mirror_loader import MirrorLoader
from surface_analysis.plotter import Plotter
from surface_analysis.points_to_mesh_converter import PointsToMeshConverter
from surface_analysis.slope_error import SlopeErrorCalculator


def main():
    ml = MirrorLoader()
    x, y, z = ml.from_leica(
        r"C:\Users\ACU005\CSIRO\ASTRI P11 Heliostats - HelioCon\HeliostatMetrology\HelioJigScans\surface_C_manually_cleaned.txt"
    )

    lt = LinearTerms()
    fitter = LinearLeastSquaresFitter()
    circular_paraboloid_terms = lt.circular_paraboloid()
    circular_paraboloid_coeffs = fitter.fit_linear_function(x, y, z, circular_paraboloid_terms)
   
    print("Paraboloid Coefficients")
    print(circular_paraboloid_coeffs)

    assembler = LinearFunctionAssembler()
    circular_paraboloid_func = assembler.assemble_linear_function(circular_paraboloid_terms, circular_paraboloid_coeffs)
    gt = GradientTerms()
    gradient_terms_x, gradient_terms_y = gt.circular_paraboloid()
    gradient_func_x, gradient_func_y = assembler.assemble_gradient_function(
        gradient_terms_x,
        gradient_terms_y,
        circular_paraboloid_coeffs,
    )
    normal_func = assembler.assemble_normal_function(
        gradient_func_x,
        gradient_func_y,
    )

    residual = z - circular_paraboloid_func(x, y)

    p2m = PointsToMeshConverter()
    x_c, y_c, z_c, area, n = p2m.points_to_normals(x, y, z)

    sec = SlopeErrorCalculator()

    angular_differences = sec.calculate_angular_differences(
        x_c,
        y_c,
        n,
        normal_func,
    )

    combined = np.hstack([angular_differences, area])
    ordered = combined[combined[:, 0].argsort()]
    angular_differences = ordered[:, 0]
    area = ordered[:, 1]

    print("Trimming top 0.5% (outliers)")
    count = len(angular_differences)
    # cutoff = round(count * 99.5 / 100)
    cutoff = count
    kept = angular_differences[:cutoff]
    removed = angular_differences[cutoff:]
    kept_np = kept.reshape(-1, 1)
    kept_area = area[:cutoff].reshape(-1, 1)
    mini = kept_np.min()
    maxi = kept_np.max()
    print(f"Removed from plot: {removed}")

    plotter = Plotter()
    bin_count = 5000
    plotter.plot_hist(kept_np, bin_count)

    print("Estimates of sigma parameter in rayleigh")

    weighted_angular_differences = kept_np * kept_area
    weighted_mean = np.sum(weighted_angular_differences) / np.sum(kept_area)
    mean_sigma = weighted_mean / np.sqrt(np.pi / 2)
    print(f"Weighted Mean = {weighted_mean} gives sigma = {mean_sigma}")

    weighted_squared_angular_differences = np.square(kept_np) * kept_area
    mean_square = np.sum(weighted_squared_angular_differences) / np.sum(kept_area)
    rms = np.sqrt(mean_square)
    mle_sigma = rms / np.sqrt(2)
    print(f"Weighted RMS = {rms} gives MLE (neglecting correction) = {mle_sigma}")

    bin_edges = np.linspace(mini, maxi, bin_count + 1)
    h, _ = np.histogram(kept_np, bin_edges)
    mode_sigma = (bin_edges[h.argmax()] + bin_edges[h.argmax() + 1]) / 2
    print(f"Mode with top 0.5% removed and {bin_count} bins = {mode_sigma}")

    plotter.plot_hist_and_curve(kept_np, mean_sigma, mle_sigma, mode_sigma, bin_count)


    cdf_data = stats.rayleigh.pdf(bin_edges, mle_sigma)
    print(cdf_data)

    

    # kst0 = stats.kstest(h, "rayleigh", args=[mle_sigma])
    # print(kst0)
    # kst1 = stats.kstest(h, "rayleigh", args=[mean_sigma])
    # print(kst1)
    # kst2 = stats.kstest(h, "rayleigh", args=[mode_sigma])
    # print(kst2)


    # np.divide(angular_differences, 

    # print("slope_error_mean")
    # sec = SlopeErrorCalculator()
    # slope_error_mean = sec.slope_error_weighted_mean(
    #     mirror.facets["x"].to_numpy().reshape(-1, 1),
    #     mirror.facets["y"].to_numpy().reshape(-1, 1),
    #     mirror.facets[["nx", "ny", "nz"]].to_numpy(),
    #     mirror.facets["area"].to_numpy().reshape(-1, 1),
    #     normal_func,
    # )
    # print(slope_error_mean)
    # print("")

    # print("Plotting mirror and fit diff")
    # print("")
    # mp.plot_mirror_and_3d_func_diff(mirror, paraboloid_func)




if __name__ == "__main__":
    main()


    # x = np.array(
    #     [
    #         [0],
    #         [1],
    #         [0],
    #         [1],
    #     ]
    # )
    # y = np.array(
    #     [
    #         [0],
    #         [0],
    #         [1],
    #         [1],
    #     ]
    # )

    # slope_error_rms = sec.slope_error_weighted_rms(
    #     mirror.facets["x"].to_numpy().reshape(-1, 1),
    #     mirror.facets["y"].to_numpy().reshape(-1, 1),
    #     mirror.facets[["nx", "ny", "nz"]].to_numpy(),
    #     mirror.facets["area"].to_numpy().reshape(-1, 1),
    #     normal_func,
    # )
    # print("slope_error_rms")
    # print(slope_error_rms)
    # print("")







    # # Get x y z offset from circular paraboloid
    # x_0 = fit_coeffs[1, 0] / (2 * fit_coeffs[0, 0])
    # y_0 = fit_coeffs[2, 0] / (2 * fit_coeffs[0, 0])
    # z_0 = -1 * (fit_coeffs[1, 0]**2 + fit_coeffs[2, 0]**2) / (4 * fit_coeffs[0, 0]) + fit_coeffs[3, 0]

    # # Want the right x, y, z offsets 
    # focalLength = 18
    # a = 1 / (4 * focalLength)
    # ideal_coeffs = np.array([
    #     a,
    #     2 * a * x_0,
    #     2 * a * y_0,
    #     a * x_0**2 + a * y_0**2 + z_0,
    # ]).reshape(-1, 1)







    # ml = MirrorLoader()
    # x, y, z = ml.from_leica(
    #     r"C:\Users\ACU005\CSIRO\ASTRI P11 Heliostats - HelioCon\HeliostatMetrology\HelioJigScans\surface_C_manually_cleaned.txt",
    # )

    # max_z = z.max()
    # min_z = z.min()
    # surface_plotter = Plotter([min_z, max_z])

    # print("Plotting mirror surface")
    # surface_plotter.plot_points_as_surface(x, y, z)
    # print("")

    # print("Fitting circular paraboloid")
    # lt = LinearTerms()
    # circular_paraboloid_terms = lt.centred_circular_paraboloid_with_z_offset()
    # general_paraboloid_terms = lt.general_paraboloid()
    # high_order_poly_terms = lt.high_order_poly()
    # fitter = LinearLeastSquaresFitter()
    # circular_paraboloid_coeffs = fitter.fit_linear_function(x, y, z, circular_paraboloid_terms)
    # general_paraboloid_coeffs = fitter.fit_linear_function(x, y, z, general_paraboloid_terms)
    # high_order_poly_coeffs = fitter.fit_linear_function(x, y, z, high_order_poly_terms)
    # print("")

    # print("General Paraboloid Coefficients")
    # print(general_paraboloid_coeffs)
    # print("")

    # print("High Order Poly Coefficients")
    # print(high_order_poly_coeffs)
    # print("")

    # print("Assembling linear functions")
    # assembler = LinearFunctionAssembler()
    # fit_circular_paraboloid = assembler.assemble_linear_function(circular_paraboloid_terms, circular_paraboloid_coeffs)
    # fit_general_paraboloid = assembler.assemble_linear_function(general_paraboloid_terms, general_paraboloid_coeffs)
    # fit_high_order_poly = assembler.assemble_linear_function(high_order_poly_terms, high_order_poly_coeffs)
    # print("")

    # print("Plotting real and high order poly fit")
    # surface_plotter.plot_points_as_surface_pair(x, y, z, fit_high_order_poly(x, y))
    # print("")

    # print("Calculating residual real - high order poly fit")
    # residual = z - fit_circular_paraboloid(x, y)
    # print("")

    # print("Plotting residual")
    # residual_plotter = Plotter()
    # residual_plotter.plot_points_as_surface(x, y, residual)
    # print("")

    # print("Making twist, focal and ideal functions")
    # fit_twist = assembler.assemble_linear_function(
    #     general_paraboloid_terms,
    #     np.array([
    #         0,
    #         0,
    #         0,
    #         0,
    #         general_paraboloid_coeffs[4, 0],
    #         0,
    #     ]).reshape(-1, 1),
    # )
    # fit_focal = assembler.assemble_linear_function(
    #     general_paraboloid_terms,
    #     np.array([
    #         general_paraboloid_coeffs[0, 0],
    #         0,
    #         general_paraboloid_coeffs[2, 0],
    #         0,
    #         0,
    #         0,
    #     ]).reshape(-1, 1),
    # )

    # focalLength = 18
    # a = 1 / (4 * focalLength)
    # fit_ideal = assembler.assemble_linear_function(
    #     general_paraboloid_terms,
    #     np.array([
    #         a,
    #         0,
    #         a,
    #         0,
    #         0,
    #         0,
    #     ]).reshape(-1, 1),
    # )

    # curve_error = fit_high_order_poly(x, y) - fit_general_paraboloid(x, y)
    # twist_error = fit_twist(x, y)
    # focal_error = fit_focal(x, y) - fit_ideal(x, y)

    # max_z = max([max(curve_error), max(twist_error), max(focal_error), max(residual)])
    # min_z = min([min(curve_error), min(twist_error), min(focal_error), min(residual)])

    # surface_plotter.z_lim = [min_z, max_z]
    # surface_plotter.plot_points_as_surface_four(x, y, curve_error, twist_error, focal_error, residual)

    # print("Assemling normal function")
    # gt = GradientTerms()
    # gradient_terms_x, gradient_terms_y = gt.circular_paraboloid()
    # gradient_func_x, gradient_func_y = assembler.assemble_gradient_function(
    #     gradient_terms_x,
    #     gradient_terms_y,
    #     general_paraboloid_terms,
    # )
    # normal_func = assembler.assemble_normal_function(
    #     gradient_func_x,
    #     gradient_func_y,
    # )

    

    # print("slope_error_mean")
    # sec = SlopeErrorCalculator()
    # slope_error_mean = sec.slope_error_weighted_mean(
    #     mirror.facets["x"].to_numpy().reshape(-1, 1),
    #     mirror.facets["y"].to_numpy().reshape(-1, 1),
    #     mirror.facets[["nx", "ny", "nz"]].to_numpy(),
    #     mirror.facets["area"].to_numpy().reshape(-1, 1),
    #     normal_func,
    # )
    # print(slope_error_mean)
    # print("")