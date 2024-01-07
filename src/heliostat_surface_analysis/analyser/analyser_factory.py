from heliostat_surface_analysis.config.analyser_option import AnalyserOption
from heliostat_surface_analysis.config.analyser_option import AnalyserOptionName
from heliostat_surface_analysis.analyser.fit_surface_analyser import FitSurfaceAnalyser
from heliostat_surface_analysis.analyser.fixed_focal_length_analyser import FixedFocalLengthAnalyser

class AnalyserFactory:
    @classmethod
    def get_analyser(cls, option: AnalyserOption):
        if option.name == AnalyserOptionName.fit_surface:
            return FitSurfaceAnalyser(option.params)
        elif option.name == AnalyserOptionName.fixed_focal_length:
            return FixedFocalLengthAnalyser(option.params)
        else:
            raise RuntimeError("analyser not recognised")
