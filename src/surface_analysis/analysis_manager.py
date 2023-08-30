import os

import pandas as pd

import typing

from surface_analysis.config.config import Config
from surface_analysis.loader.loader import Loader
from surface_analysis.loader.loader_factory import LoaderFactory
from surface_analysis.analyzer.analyzer import Analyzer
from surface_analysis.analyzer.analyzer_factory import AnalyzerFactory
from surface_analysis.preprocessor.preprocessor import Preprocessor
from surface_analysis.preprocessor.preprocessor_factory import PreprocessorFactory


class AnalysisManager:
    def analyze_scans(
        self,
        config: Config,
        scans_dir: str,
        output_dir: str,
    ) -> list:
        loader = LoaderFactory.get_loader(config.loader)
        preprocessor = PreprocessorFactory.get_preprocessor(config.preprocessor)
        analyzer = AnalyzerFactory.get_analyser(config.analyzer,output_dir)

        analysis_results = []
        for scan_file in os.listdir(scans_dir):
            scan_path = os.path.join(scans_dir, scan_file)
            analysis_result = self.analyze_scan(
                scan_path,
                loader,
                preprocessor,
                analyzer,
            )
            print(scan_file, analysis_result)
            analysis_results.append(analysis_result)
        return analysis_results

    def analyze_scan(
        self,
        scan_path: str,
        loader: Loader,
        preprocessor: Preprocessor,
        analyzer: Analyzer,
    ) -> pd.DataFrame:
        scan_name = os.path.splitext(os.path.basename(scan_path))[0]
        raw_x, raw_y, raw_z = loader.load_points(scan_path)
        x, y, z = preprocessor.preprocess_points(raw_x, raw_y, raw_z)       
        analysis = analyzer.analyze(x, y, z, scan_name)
        return analysis
