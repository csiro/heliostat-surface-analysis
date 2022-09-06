from surface_analysis.mirror_fitter import MirrorFitter
from surface_analysis.mirror_loader import MirrorLoader
from surface_analysis.mirror_plotter import MirrorPlotter


def main():
    # mirror = MirrorLoader.from_leica(
    #     "cal_mirror",
    #     40.0,
    #     r"C:\Users\ACU005\CSIRO\ASTRI P11 Heliostats - HelioCon\HeliostatMetrology\HelioJigScans\surface_C_manually_cleaned.txt",
    # )
    mirror_old = MirrorLoader.from_csv(
        "cal_mirror",
        40.0,
        r"C:\Users\ACU005\CSIRO\ASTRI P11 Heliostats - HelioCon\HeliostatMetrology\HelioJigScans\surface_old_2012_scan_cleaned.csv",
    )

    mirror_new = MirrorLoader.from_leica(
        "cal_mirror",
        40.0,
        r"C:\Users\ACU005\CSIRO\ASTRI P11 Heliostats - HelioCon\HeliostatMetrology\HelioJigScans\surface_C_manually_cleaned.txt",
    )

    # MirrorPlotter.plot_mirror_3d(mirror)

    # coeff0, func0 = MirrorFitter.fit_centred_circular_paraboloid(mirror.points)
    # _, func1 = MirrorFitter.fit_centred_circular_paraboloid_with_z_offset(mirror.points)
    coeff0, func0 = MirrorFitter.fit_circular_paraboloid(mirror_old.points)
    coeff1, func1 = MirrorFitter.fit_circular_paraboloid(mirror_new.points)
    print(coeff0)
    print(coeff1)
    
    coeff0 = MirrorFitter.fit_1d_parabola_radially(mirror_old.points)
    coeff1 = MirrorFitter.fit_1d_parabola_radially(mirror_new.points)
    print(coeff0)
    print(coeff1)

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
