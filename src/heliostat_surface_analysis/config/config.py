from pydantic import BaseModel

from heliostat_surface_analysis.config.loader_option import LoaderOption
from heliostat_surface_analysis.config.preprocessor_option import PreprocessorOption
from heliostat_surface_analysis.config.mesher_option import MesherOption
from heliostat_surface_analysis.config.analyser_option import AnalyserOption
from heliostat_surface_analysis.config.aggregator_option import AggregatorOption


class Config(BaseModel):
    loader: LoaderOption
    preprocessor: PreprocessorOption
    mesher: MesherOption
    analyser: AnalyserOption
    aggregator: AggregatorOption
