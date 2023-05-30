from surface_analysis.config.analyzer_option import AnalyzerOption
from surface_analysis.config.analyzer_option import AnalyzerOptionName
from surface_analysis.analyzer.basic_analyzer import BasicAnalyzer

class AnalyzerFactory:
    @classmethod
    def get_analyser(cls, option: AnalyzerOption):
        if option.name == AnalyzerOptionName.basic:
            return BasicAnalyzer()
        else:
            return BasicAnalyzer()
