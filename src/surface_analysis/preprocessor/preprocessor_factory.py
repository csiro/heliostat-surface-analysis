from typing import Optional

from surface_analysis.config import PreprocessorOption
from surface_analysis.preprocessor.no_preprocessor import NoPreprocessor
from surface_analysis.preprocessor.basic_preprocessor import BasicPreprocessor
from surface_analysis.preprocessor.outlier_preprocessor import OutlierPreprocessor


class PreprocessorFactory:
    @classmethod
    def get_preprocessor(cls, option: Optional[PreprocessorOption]):
        if option == PreprocessorOption.no:
            return NoPreprocessor()
        elif option == PreprocessorOption.basic:
            return BasicPreprocessor()
        elif option == PreprocessorOption.outlier:
            return OutlierPreprocessor()
        else:
            return BasicPreprocessor()
