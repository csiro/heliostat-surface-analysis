from surface_analysis.config.analyzer_option import AnalyzerOption
from surface_analysis.config.analyzer_option import AnalyzerOptionName
from surface_analysis.analyzer.basic_analyzer import BasicAnalyzer
from surface_analysis.analyzer.fit_curve_analyzer import FitCurveAnalyzer

class AnalyzerFactory:
    @classmethod
    def get_analyser(cls, option: AnalyzerOption):
        if option.name == AnalyzerOptionName.basic:
            return BasicAnalyzer(option.params)
        elif option.name == AnalyzerOptionName.fit_curve:
            return FitCurveAnalyzer(option.params)
        else:
            return BasicAnalyzer()
