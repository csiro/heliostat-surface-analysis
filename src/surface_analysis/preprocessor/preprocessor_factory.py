from surface_analysis.config.preprocessor_option import PreprocessorOption
from surface_analysis.config.preprocessor_option import PreprocessorOptionName
from surface_analysis.preprocessor.no_preprocessor import NoPreprocessor
from surface_analysis.preprocessor.basic_preprocessor import BasicPreprocessor
from surface_analysis.preprocessor.outlier_preprocessor import OutlierPreprocessor


class PreprocessorFactory:
    @classmethod
    def get_preprocessor(cls, option: PreprocessorOption):
        if option.name == PreprocessorOptionName.none:
            return NoPreprocessor()
        elif option.name == PreprocessorOptionName.basic:
            return BasicPreprocessor()
        elif option.name == PreprocessorOptionName.outlier:
            return OutlierPreprocessor()
        else:
            return BasicPreprocessor()
