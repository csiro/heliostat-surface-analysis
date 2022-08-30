from mirror_surface_plotter import MirrorSurface


def main():
    mirror = MirrorSurface(
        "cal_mirror",
        40.0,
        r"C:\Users\ACU005\CSIRO\ASTRI P11 Heliostats - HelioCon\HeliostatMetrology\HelioJigScans\surface_C.txt",
    )
    mirror.fit_circular_paraboloid(mirror.points)

if __name__ == "__main__":
    main()
