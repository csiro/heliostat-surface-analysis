import numpy as np
import matplotlib.pyplot as plt

from surface_analysis.preprocessor.basic_preprocessor import BasicPreprocessor


class KnownSizePreprocessor(BasicPreprocessor):
    def preprocess_points(
        self,
        raw_x: np.ndarray,
        raw_y: np.ndarray,
        raw_z: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        x, y, z = super().preprocess_points(raw_x, raw_y, raw_z)
        return self.rotate_xy_plane(x, y, z)

    def rotate_xy_plane(
        self,
        raw_x: np.ndarray,
        raw_y: np.ndarray,
        raw_z: np.ndarray,
        width: float,
        height: float,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        fig, ax = plt.subplots()
        ax.scatter(raw_x, raw_y)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        exit()        

        return raw_x, raw_y, raw_z
