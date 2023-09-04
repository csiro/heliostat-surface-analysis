import numpy as np

from typing import Union, Optional, cast, Dict, Tuple

from surface_analysis.preprocessor.basic_preprocessor import BasicPreprocessor
from surface_analysis.fitter.fitter import NonLinearFitter
from surface_analysis.objective.linear_objective_function import XYPlaneOrientationObjectiveFunction

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
        x, y, z = super().preprocess_points(raw_x, raw_y, raw_z)
        return self.rotate_xy_plane(x, y, z)

    def rotate_xy_plane(
        self,
        raw_x: np.ndarray,
        raw_y: np.ndarray,
        raw_z: np.ndarray,
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        func_class = XYPlaneOrientationObjectiveFunction(raw_x,raw_y,raw_z,self.width,self.height)
        fitter = NonLinearFitter(1,func_class,[0],[2*np.pi],[0])
        params = fitter.fit()
        x,y,z = func_class.rotate_points(params[0][0])
        
        return x,y,z
