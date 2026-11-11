import os

import pandas as pd
import progressbar
import stl

import typing

from heliostat_surface_analysis.config.config import Config
from heliostat_surface_analysis.loader.loader import Loader
from heliostat_surface_analysis.loader.loader_factory import LoaderFactory
from heliostat_surface_analysis.preprocessor.preprocessor import Preprocessor
from heliostat_surface_analysis.preprocessor.preprocessor_factory import PreprocessorFactory
from heliostat_surface_analysis.mesher.mesher import Mesher
from heliostat_surface_analysis.mesher.mesher_factory import MesherFactory
from heliostat_surface_analysis.analyser.analyser import Analyser
from heliostat_surface_analysis.analyser.analyser_factory import AnalyserFactory
from heliostat_surface_analysis.aggregator.aggregator import Aggregator
from heliostat_surface_analysis.aggregator.aggregator_factory import AggregatorFactory
from heliostat_surface_analysis.plotting.plotting import plot_points_3d, plot_2d_surface


class AnalysisManager:
    @staticmethod
    def analyse_scans(
        config: Config,
        scans_dir: str,
        output_dir: str,
        plot: bool,
        write_stls: bool
    ) -> list:
        loader = LoaderFactory.get_loader(config.loader)
        preprocessor = PreprocessorFactory.get_preprocessor(config.preprocessor)
        mesher = MesherFactory.get_mesher(config.mesher)
        analyser = AnalyserFactory.get_analyser(config.analyser)
        aggregator = AggregatorFactory.get_aggregator(config.aggregator)

        analysis_results = []
        scan_files = sorted(f for f in os.listdir(scans_dir) if f.lower().endswith((".txt", ".csv")))
        bar = progressbar.ProgressBar(maxval=len(scan_files)).start()
        for i,scan_file in enumerate(scan_files):
            scan_path = os.path.join(scans_dir, scan_file)
            analysis_result = AnalysisManager.analyse_scan(
                scan_path,
                loader,
                preprocessor,
                mesher,
                analyser,
                aggregator,
                output_dir,
                plot,
                write_stls,
            )
            analysis_results.append(analysis_result)
            bar.update(i+1)
        bar.finish()
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
        plot: bool,
        write_stls: bool,
    ) -> pd.DataFrame:
        scan_name = os.path.splitext(os.path.basename(scan_path))[0]
        raw_x, raw_y, raw_z = loader.load_points(scan_path)
        x, y, z = preprocessor.preprocess_points(raw_x, raw_y, raw_z)
        if plot:
            plot_points_3d(raw_x,raw_y,raw_z,x,y,z,title=scan_name)
        mesh = mesher.create_mesh(x, y, z)
        if write_stls:
            filepath = os.path.join(output_dir,f"{scan_name}.stl")
            mesh.save(filepath, mode=stl.Mode.BINARY)
            print("Created: %s"%filepath)
        areas, normals, coeffs, ideal_normals, ideal_zs, slope_errors = analyser.analyse(x, y, z, mesh, scan_name)
        if plot:
            plot_2d_surface(mesh,slope_errors,label="slope error (rad)",ax=None)
        aggregate = aggregator.aggregate(slope_errors,areas)

        result = {}
        result["name"] = scan_name
        result["aggregate"] = aggregate
        for i,label in enumerate(analyser.get_coefficient_labels()):
            result["coeff: %s"%label] = coeffs[i][0]
        # result["surface coefficients"] = coeffs # .reshape(-1, 1)
        result["samples"] = len(areas)
        result["area"] = sum(areas)[0]

        return result
