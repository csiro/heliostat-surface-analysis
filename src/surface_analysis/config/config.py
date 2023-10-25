from pydantic import BaseModel

from surface_analysis.config.loader_option import LoaderOption
from surface_analysis.config.preprocessor_option import PreprocessorOption
from surface_analysis.config.analyzer_option import AnalyzerOption
from surface_analysis.config.aggregator_option import AggregatorOption


class Config(BaseModel):
    loader: LoaderOption
    preprocessor: PreprocessorOption
    analyzer: AnalyzerOption
    aggregator: AggregatorOption
