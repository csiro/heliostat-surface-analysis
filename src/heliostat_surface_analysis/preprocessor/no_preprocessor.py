import numpy as np
import typing

from heliostat_surface_analysis.preprocessor.preprocessor import Preprocessor


class NoPreprocessor(Preprocessor):
    def preprocess_points(
        self,
        raw_x: np.ndarray,
        raw_y: np.ndarray,
        raw_z: np.ndarray,
    ) -> typing.Tuple[np.ndarray, np.ndarray, np.ndarray]:
        return (raw_x, raw_y, raw_z)
