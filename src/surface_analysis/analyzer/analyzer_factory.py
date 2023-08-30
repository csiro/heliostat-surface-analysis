from surface_analysis.config.analyzer_option import AnalyzerOption
from surface_analysis.config.analyzer_option import AnalyzerOptionName
from surface_analysis.analyzer.basic_analyzer import BasicAnalyzer
from surface_analysis.analyzer.fit_surface_analyzer import FitSurfaceAnalyzer
from surface_analysis.analyzer.known_focal_analyzer import KnownFocalAnalyzer

class AnalyzerFactory:
    @classmethod
    def get_analyser(cls, option: AnalyzerOption):
        if option.name == AnalyzerOptionName.basic:
            return BasicAnalyzer(option.params)
        elif option.name == AnalyzerOptionName.fit_surface:
            return FitSurfaceAnalyzer(option.params)
        elif option.name == AnalyzerOptionName.known_focal:
            return KnownFocalAnalyzer(option.params)           
        else:
            raise RuntimeError("analyzer not recognised")
