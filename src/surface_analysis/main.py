from surface_analysis.analysis import analyse_scans
from surface_analysis.loaders.leica_loader import LeicaLoader
from surface_analysis.loaders.default_loader import DefaultLoader
from surface_analysis.loaders.scaling_loader import ScalingLoader
from surface_analysis.preprocessors.outlier_preprocessor import OutlierPreprocessor
# from functools import partial
# from surface_analysis.fitters.fitter import linear_least_squares_fit
# from surface_analysis.fitters.fitter import non_linear_fit
# from surface_analysis.linear_functions.circular_paraboloid import CircularParaboloid


def main():
    analyse_scans(
        input_path=r"C:\Users\ACU005\CSIRO\ASTRI P11 Heliostats - HelioCon\HeliostatMetrology\old-scans\newcastle-field-2",
        # input_path=r"C:\Users\ACU005\CSIRO\ASTRI P11 Heliostats - HelioCon\HeliostatMetrology\test-scans",
        output_path="outputs",
        loader=ScalingLoader(),
        preprocessor=OutlierPreprocessor(),
    )

    # x, y, z = LeicaLoader().load_points(r"C:\Users\ACU005\CSIRO\ASTRI P11 Heliostats - HelioCon\HeliostatMetrology\new-scans\scans\surface-d.txt")
    # x, y, z = OutlierPreprocessor().preprocess_points(x, y, z)
    # terms = CircularParaboloid().terms
    # a = partial(linear_least_squares_fit, x=x, y=y, z=z)
    # b = partial(linear_least_squares_fit, terms=terms)
    # print(a(terms=terms))
    # print(b(x, y, z))


if __name__ == "__main__":
    main()
