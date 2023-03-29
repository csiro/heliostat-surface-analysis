import numpy as np

from surface_analysis.preprocessors.preprocessor import Preprocessor


class NoPreprocessor(Preprocessor):
    def preprocess_points(
        self,
        raw_x: np.ndarray,
        raw_y: np.ndarray,
        raw_z: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        return (raw_x, raw_y, raw_z)
