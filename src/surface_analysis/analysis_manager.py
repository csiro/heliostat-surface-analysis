import os

import pandas as pd

import typing

from surface_analysis.config.config import Config
from surface_analysis.loader.loader import Loader
from surface_analysis.loader.loader_factory import LoaderFactory
from surface_analysis.preprocessor.preprocessor import Preprocessor
from surface_analysis.preprocessor.preprocessor_factory import PreprocessorFactory
from surface_analysis.mesher.mesher import Mesher
from surface_analysis.mesher.mesher_factory import MesherFactory
from surface_analysis.analyser.analyser import Analyser
from surface_analysis.analyser.analyser_factory import AnalyserFactory
from surface_analysis.aggregator.aggregator import Aggregator
from surface_analysis.aggregator.aggregator_factory import AggregatorFactory
from surface_analysis.plotting.plotting import plot_points_3d


class AnalysisManager:
    @staticmethod
    def analyse_scans(
        config: Config,
        scans_dir: str,
        output_dir: str,
        plot_points: bool,
        write_stls: bool
    ) -> list:
        loader = LoaderFactory.get_loader(config.loader)
        preprocessor = PreprocessorFactory.get_preprocessor(config.preprocessor)
        mesher = MesherFactory.get_mesher(config.mesher)
        analyser = AnalyserFactory.get_analyser(config.analyser)
        aggregator = AggregatorFactory.get_aggregator(config.aggregator)

        analysis_results = []
        for scan_file in sorted(os.listdir(scans_dir)):
            scan_path = os.path.join(scans_dir, scan_file)
            analysis_result = AnalysisManager.analyse_scan(
                scan_path,
                loader,
                preprocessor,
                mesher,
                analyser,
                aggregator,
                output_dir,
                plot_points,
                write_stls,
            )
            print(analysis_result)
            analysis_results.append(analysis_result)
        return analysis_results

    @staticmethod
    def analyse_scan(
        scan_path: str,
        loader: Loader,
        preprocessor: Preprocessor,
        mesher: Mesher,
        analyser: Analyser,
        aggregator: Aggregator,
        output_dir: str,
        plot_points: bool,
        write_stls: bool,
    ) -> pd.DataFrame:
        scan_name = os.path.splitext(os.path.basename(scan_path))[0]
        raw_x, raw_y, raw_z = loader.load_points(scan_path)
        x, y, z = preprocessor.preprocess_points(raw_x, raw_y, raw_z)
        if plot_points:
            plot_points_3d(raw_x,raw_y,raw_z,x,y,z,title=scan_name)
        mesh = mesher.create_mesh(x, y, z)
        if write_stls:
            mesh.save(os.path.join(output_dir,f"{scan_name}.stl"))
        areas, normals, coeffs, ideal_normals, slope_errors = analyser.analyse(x, y, z, mesh, scan_name)
        aggregate = aggregator.aggregate(slope_errors,areas)
        
        result = {}
        result["name"] = scan_name
        result["aggregate"] = aggregate
        result["coeffs"] = coeffs
        result["samples"] = len(areas)
        
        return result
