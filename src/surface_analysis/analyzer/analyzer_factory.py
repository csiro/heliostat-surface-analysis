from surface_analysis.config.analyzer_option import AnalyzerOption
from surface_analysis.config.analyzer_option import AnalyzerOptionName
from surface_analysis.analyzer.basic_analyzer import BasicAnalyzer
from surface_analysis.analyzer.supplied_reference_analyzer import SuppliedReferenceAnalyzer

class AnalyzerFactory:
    @classmethod
    def get_analyser(cls, option: AnalyzerOption):
        if option.name == AnalyzerOptionName.basic:
            return BasicAnalyzer()
        elif option.name == AnalyzerOptionName.supplied_reference:
            return SuppliedReferenceAnalyzer(option.params)
        else:
            return BasicAnalyzer()
