from typing import Optional

from surface_analysis.config.config import AnalyzerOption
from surface_analysis.analyzer.basic_analyzer import BasicAnalyser

class AnalyserFactory:
    @classmethod
    def get_analyser(cls, option: Optional[AnalyzerOption]):
        if option == AnalyzerOption.basic:
            return BasicAnalyser()
        else:
            return BasicAnalyser()
