import numpy as np

from typing import Union, Optional, cast, Dict, Tuple

from surface_analysis.preprocessor.basic_preprocessor import BasicPreprocessor

class KnownSizePreprocessor(BasicPreprocessor):
    def __init__(
        self,
        params: Optional[Dict[str, Union[str, float]]],
    ):
        params = cast(Dict[str, Union[str, float]], params)
        width = float(params["width"])
        height = float(params["height"])
        self.width = width
        self.height = height

    def preprocess_points(
        self,
        raw_x: np.ndarray,
        raw_y: np.ndarray,
        raw_z: np.ndarray,
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    	# NOTE: currently just applying the method from BasicPreprocessor
        return super().preprocess_points(raw_x, raw_y, raw_z)
