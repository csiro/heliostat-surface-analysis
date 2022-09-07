from turtle import position
import numpy as np

from surface_analysis.slope_error import calculate_angular_differences, slope_error_weighted_mean, slope_error_weighted_rms
from surface_analysis import mirror_loader
from surface_analysis.linear_least_squares_fitter import LinearLeastSquaresFitter
from surface_analysis.mirror_loader import from_csv, from_leica
from surface_analysis.mirror_plotter import MirrorPlotter


def main():
    x = np.array([
        [0],
        [1],
        [2]
    ])
    y = np.array([
        [1],
        [0],
        [0]
    ])
    z = np.array([
        [1],
        [1],
        [4]
    ])
    terms = [
        lambda x, y: x**2,
        lambda x, y: y**2,
        lambda x, y: x * 0 + 1
    ]

    fitter = LinearLeastSquaresFitter()
    coeffs = fitter.fit_linear_function(x, y, z, terms)

    paraboloid_func = fitter.assemble_linear_function(
        terms,
        coeffs
    )

    print(paraboloid_func(x, y))

    # mirror = from_leica(
    #     "cal_mirror",
    #     40.0,
    #     r"C:\Users\ACU005\CSIRO\ASTRI P11 Heliostats - HelioCon\HeliostatMetrology\HelioJigScans\surface_C_manually_cleaned.txt",
    # )



    # def vertical_func(positions: np.ndarray) -> np.ndarray:
    #     position_count = positions.shape[0]
    #     zeros = np.zeros((position_count, 2))
    #     ones = np.ones((position_count, 1))
    #     return np.hstack((zeros, ones))

    # mean_error = slope_error_weighted_mean(
    #     mirror.facets[["x", "y"]].to_numpy(),
    #     mirror.facets[["nx", "ny", "nz"]].to_numpy(),
    #     mirror.facets["area_xy"].to_numpy().reshape(-1, 1),
    #     vertical_func
    # )
    # rms_error = slope_error_weighted_rms(
    #     mirror.facets[["x", "y"]].to_numpy(),
    #     mirror.facets[["nx", "ny", "nz"]].to_numpy(),
    #     mirror.facets["area_xy"].to_numpy().reshape(-1, 1),
    #     vertical_func
    # )
    # print(mean_error)
    # print(rms_error)



    # print("")
    # print("Fitting general paraboloid")
    # coeff0, func0 = MirrorFitter.fit_general_paraboloid(mirror.points)
    # print("Function: z = ax^2 + bx + cy^2 + dy + exy + f")
    # print(f"a = {round(coeff0[0], 4)}, b = {round(coeff0[1], 4)}, c = {round(coeff0[2], 4)}, d = {round(coeff0[3], 4)}, e = {round(coeff0[4], 4)}, f = {round(coeff0[5], 4)}")
    # print(f"fx = {round(1/(4*coeff0[0]), 4)}m, fy = {round(1/(4*coeff0[2]), 4)}m")
    # print(f"Residual slope error mean = {}")
    # print(f"Residual slope error RMS = {}")

    # print("")
    # print("Fitting high order curve")
    # print("z = ax^2y^2 + bx^2y + cx^2 + dxy^2 + exy + fx + gy^2 + hy + i")
    # coeff1, func1 = MirrorFitter.fit_high_order_poly(mirror.points)
    # print(f"a = {round(coeff1[0], 4)}, b = {round(coeff1[1], 4)}, c = {round(coeff1[2], 4)}, d = {round(coeff1[3], 4)}, e = {round(coeff1[4], 4)}, f = {round(coeff1[5], 4)}, g = {round(coeff1[6], 4)}, h = {round(coeff1[7], 4)}, i = {round(coeff1[8], 4)}")
    # print(f"fx = {round(1/(4*coeff1[2]), 4)}m, fy = {round(1/(4*coeff1[6]), 4)}m")
    # print(f"Residual slope error mean = {}")
    # print(f"Residual slope error RMS = {}")

    # positions = np.array([
    #     [1, 0],
    #     [0, 1],
    #     [1, 1]
    # ])
    # normals = np.array([
    #     [0, 0, 0],
    #     [0, 1, 1],
    #     [1, 1, 1]
    # ])



    # error = calculate_angular_differences(positions, normals, vertical_func)


    # coeff0, func0 = MirrorFitter.fit_centred_circular_paraboloid(mirror.points)
    # coeff1, func1 = MirrorFitter.fit_centred_circular_paraboloid_with_z_offset(mirror.points)
    # coeff2, func2 = MirrorFitter.fit_circular_paraboloid(mirror.points)
    # coeff3, func3 = MirrorFitter.fit_elliptic_paraboloid(mirror.points)
    # coeff4, func4 = MirrorFitter.fit_general_paraboloid(mirror.points)
    # coeff5, func5 = MirrorFitter.fit_high_order_poly(mirror.points)
    # coeff6 = MirrorFitter.fit_1d_parabola_radially(mirror.points)

    # mirror_old = from_csv(
    #     "cal_mirror",
    #     40.0,
    #     r"C:\Users\ACU005\CSIRO\ASTRI P11 Heliostats - HelioCon\HeliostatMetrology\HelioJigScans\surface_old_2012_scan_cleaned.csv",
    # )
    
    # print(f"Centred Circular a={coeff0[0]} focal={1/(4*coeff0[0])}")
    # print(f"Centred Circular with z a={coeff1[0]} focal={1/(4*coeff1[0])} z-offset={coeff1[1]}")
    # print(f"Circular a={coeff2[0]} focal={1/(4*coeff2[0])} b={coeff2[1]} c={coeff2[2]} d={coeff2[3]}")
    # print(f"Elliptic a={coeff3[0]} focal_x={1/(4*coeff3[0])} b={coeff3[1]} c={coeff3[2]} focal_y={1/(4*coeff3[2])} d={coeff3[3]} e={coeff3[4]}")
    # print(f"General a={coeff4[0]} focal_x={1/(4*coeff4[0])} b={coeff4[1]} c={coeff4[2]} focal_y={1/(4*coeff4[2])} d={coeff4[3]} e={coeff4[4]} f={coeff4[5]}")
    # print(f"High order a={coeff5[0]} b={coeff5[1]} c={coeff5[2]} focal_x={1/(4*coeff5[2])} d={coeff5[3]} e={coeff5[4]} f={coeff5[5]} g={coeff5[6]} focal_y={1/(4*coeff5[6])} h={coeff5[7]}  i={coeff5[8]}")
    # print(f"Radial a={coeff6[0]} focal={1/(4*coeff6[0])} b={coeff6[1]} c={coeff6[2]}")

    # MirrorPlotter.plot_2d_func(func0, mirror.points[["x", "y"]].to_numpy(), z_lim=[-0.01, 0.02])
    # MirrorPlotter.plot_2d_func(func1, mirror.points[["x", "y"]].to_numpy(), z_lim=[-0.01, 0.02])
    # MirrorPlotter.plot_2d_func(func2, mirror.points[["x", "y"]].to_numpy(), z_lim=[-0.01, 0.02])
    # MirrorPlotter.plot_2d_func_diff(func0, func1, mirror.points[["x", "y"]].to_numpy(), z_lim=[-0.01, 0.02])
    # MirrorPlotter.plot_2d_func(func0, mirror.points[["x", "y"]].to_numpy())
    # MirrorPlotter.plot_mirror_and_fit(mirror, eval_circular_paraboloid_eval)
    # mirror.plot()
    # mirror.plot()
    # coeffs = mirror.fit_circular_paraboloid(mirror.points)
    # mirror.fit_general_paraboloid(mirror.points)
    # mirror.plot_paraboloid()


if __name__ == "__main__":
    main()
