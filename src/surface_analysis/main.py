from surface_analysis.analysis import analyse_scans
from surface_analysis.loaders.leica_loader import LeicaLoader
from surface_analysis.loaders.default_loader import DefaultLoader
from surface_analysis.preprocessors.outlier_preprocessor import OutlierPreprocessor


def main():
    analyse_scans(
        input_path=r"C:\Users\ACU005\CSIRO\ASTRI P11 Heliostats - HelioCon\HeliostatMetrology\new-scans",
        output_path="outputs",
        loader=LeicaLoader(),
        preprocessor=OutlierPreprocessor(),
    )


if __name__ == "__main__":
    main()
