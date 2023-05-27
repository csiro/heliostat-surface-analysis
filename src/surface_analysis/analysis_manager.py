import os

import pandas as pd

from surface_analysis.config.config import Config
from surface_analysis.loader.loader import Loader
from surface_analysis.loader.loader_factory import LoaderFactory
from surface_analysis.analyser.analyser_factory import AnalyserFactory
from surface_analysis.preprocessor.preprocessor_factory import PreprocessorFactory
from surface_analysis.preprocessor.preprocessor import Preprocessor
from surface_analysis.measured_surface import MeasuredSurface
from surface_analysis.points_to_mesh_converter import points_to_normals
from surface_analysis.analyser.basic_analyser import BasicAnalyser


class AnalysisManager:
    def analyse_scans(
        self,
        config: Config,
        scans_dir: str,
    ) -> None:
        loader = LoaderFactory.get_loader(config.loader)
        preprocessor = PreprocessorFactory.get_preprocessor(config.preprocessor)
        analyser = AnalyserFactory.get_analyser(config.analysis)

        analysis_results = []
        for scan_file in os.listdir(scans_dir):
            scan_path = os.path.join(scans_dir, scan_file)

            analysis_result = self.analyse_scan(
                scan_path,
                loader,
                preprocessor,
                analyser,
            )
            analysis_results.append(analysis_result)

    def analyse_scan(
        self,
        scan_path: str,
        loader: Loader,
        preprocessor: Preprocessor,
        analyser: Analyser,
    ) -> pd.DataFrame:
        raw_x, raw_y, raw_z = loader.load_points(scan_path)
        x, y, z = preprocessor.preprocess_points(raw_x, raw_y, raw_z)
        return analyser.analyse(x, y, z)
