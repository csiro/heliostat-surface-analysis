import os

import pandas as pd

from surface_analysis.config import Config
from surface_analysis.loader.loader import Loader
from surface_analysis.loader.loader_factory import LoaderFactory
from surface_analysis.analyser.analyser_factory import AnalyserFactory
from surface_analysis.preprocessor.preprocessor_factory import PreprocessorFactory
from surface_analysis.preprocessor.preprocessor import Preprocessor
from surface_analysis.measured_surface import MeasuredSurface
from surface_analysis.points_to_mesh_converter import points_to_normals
from surface_analysis.analyser.basic_analyser import BasicAnalyser


OUTPUT_DIR = "output"


class AnalysisManager:
    def analyse_scans(
        self,
        config: Config,
        scans_dir: str,
        design_focal_lengths: dict[str, float],
        scan_files: list[str],
    ) -> None:
        analyser = AnalyserFactory.get_analyser(config.analysis)
        loader = LoaderFactory.get_loader(config.loader)
        preprocessor = PreprocessorFactory.get_preprocessor(config.preprocessor)

        analysis_results = []
        for scan_file in scan_files:
            scan_name = scan_file.split(".")[0]
            scan_output_dir = os.path.join(scans_dir, OUTPUT_DIR, scan_name)
            os.makedirs(scan_output_dir, exist_ok=True)

            analysis_result = self.analyse_scan(
                scans_dir,
                scan_file,
                scan_name,
                scan_output_dir,
                design_focal_lengths[scan_name],
                analyser,
                loader,
                preprocessor,
            )
            analysis_results.append(analysis_result)

        table = pd.DataFrame.from_records(analysis_results)
        table.to_csv(os.path.join(scans_dir, OUTPUT_DIR, "output.csv"))

    def analyse_scan(
        self,
        scans_dir: str,
        scan_file: str,
        scan_name: str,
        scan_output_dir: str,
        design_focal_length: float,
        analyser: BasicAnalyser,
        loader: Loader,
        preprocessor: Preprocessor,
    ) -> pd.DataFrame:
        scan_path = os.path.join(scans_dir, scan_file)
        surface = self.load_measured_points(scan_path, loader, preprocessor)

        return analyser.analyse(
            surface,
            scan_name,
            scan_output_dir,
            design_focal_length,
        )

    def load_measured_points(
        self,
        scan_path: str,
        loader: Loader,
        preprocessor: Preprocessor,
    ) -> MeasuredSurface:
        raw_x, raw_y, raw_z = loader.load_points(scan_path)
        x, y, z = preprocessor.preprocess_points(raw_x, raw_y, raw_z)
        x_c, y_c, z_c, area, n = points_to_normals(x, y, z)
        return MeasuredSurface(x, y, z, x_c, y_c, z_c, n, area)
