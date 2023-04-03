from typing import Optional

from surface_analysis.config import AnalysisOption
from surface_analysis.analyser.basic_analyser import BasicAnalyser

class AnalyserFactory:
    @classmethod
    def get_analyser(cls, option: Optional[AnalysisOption]):
        if option == AnalysisOption.basic:
            return BasicAnalyser()
        else:
            return BasicAnalyser()
