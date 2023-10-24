import numpy as np

from surface_analysis.loader.default_loader import DefaultLoader

from typing import Union, Optional, cast, Any, Dict, Tuple

class ScalingLoader(DefaultLoader):
    def __init__(
        self,
        params: Optional[Dict[str, Union[str, float]]]
    ):
        params = cast(Dict[str, Union[str, float]], params)
        if params["units"]=="mm":
            self.scale_factor = 1.0e-3
        else:
            raise RuntimeError("units %s not recognised"%params["units"])
    
    def load_points(self, file_path: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        x, y, z = super().load_points(file_path)
        return (
            x * self.scale_factor,
            y * self.scale_factor,
            z * self.scale_factor,
        )
