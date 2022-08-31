from surface_analysis.mirror_fitter import MirrorFitter
from surface_analysis.mirror_loader import MirrorLoader
from surface_analysis.mirror_plotter import MirrorPlotter


def main():
    mirror = MirrorLoader.from_leica(
        "cal_mirror",
        40.0,
        r"C:\Users\ACU005\CSIRO\ASTRI P11 Heliostats - HelioCon\HeliostatMetrology\HelioJigScans\surface_C_manually_cleaned.txt",
    )

    coeff = MirrorFitter.fit_circular_paraboloid(mirror.points)
    def eval_circular_paraboloid_eval(x: float, y: float):
        return coeff[0]*(x**2+y**2) + coeff[1]*x + coeff[2]*y + coeff[3]
    MirrorPlotter.plot_mirror_and_fit(mirror, eval_circular_paraboloid_eval)
    # mirror.plot()
    # mirror.plot()
    # coeffs = mirror.fit_circular_paraboloid(mirror.points)
    # mirror.fit_general_paraboloid(mirror.points)
    # mirror.plot_paraboloid()


if __name__ == "__main__":
    main()
