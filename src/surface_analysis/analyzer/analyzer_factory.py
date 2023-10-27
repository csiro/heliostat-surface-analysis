from surface_analysis.config.analyzer_option import AnalyzerOption
from surface_analysis.config.analyzer_option import AnalyzerOptionName
from surface_analysis.analyzer.fit_surface_analyzer import FitSurfaceAnalyzer
from surface_analysis.analyzer.known_focal_analyzer import KnownFocalAnalyzer
from surface_analysis.mesher.mesher import Mesher

class AnalyzerFactory:
    @classmethod
    def get_analyser(cls, option: AnalyzerOption, mesher: Mesher, output_dir: str):
        if option.name == AnalyzerOptionName.fit_surface:
            return FitSurfaceAnalyzer(option.params,mesher,output_dir)
        elif option.name == AnalyzerOptionName.known_focal:
            return KnownFocalAnalyzer(option.params,mesher,output_dir)
        else:
            raise RuntimeError("analyzer not recognised")
