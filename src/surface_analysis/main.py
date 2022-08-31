from mirror_loader import MirrorLoader
from mirror_surface_plotter import MirrorSurface


def main():
    mirror = MirrorLoader.from_leica(
        "cal_mirror",
        40.0,
        r"C:\Users\ACU005\CSIRO\ASTRI P11 Heliostats - HelioCon\HeliostatMetrology\HelioJigScans\surface_C_manually_cleaned.txt",
    )
    
    # mirror.plot()
    # mirror.plot()
    # coeffs = mirror.fit_circular_paraboloid(mirror.points)
    mirror.fit_general_paraboloid(mirror.points)
    # mirror.plot_paraboloid()


if __name__ == "__main__":
    main()
