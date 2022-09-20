from abc import ABC, abstractmethod

import numpy as np
from sklearn.decomposition import PCA


class Preprocessor(ABC):
    @abstractmethod
    def preprocess_points(
        self,
        raw_x: np.ndarray,
        raw_y: np.ndarray,
        raw_z: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        pass


class BasicPreprocessor(Preprocessor):
    def preprocess_points(
        self,
        raw_x: np.ndarray,
        raw_y: np.ndarray,
        raw_z: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        centred_x, centred_y, centred_z = self.centre_points_centroid(raw_x, raw_y, raw_z)
        return self.rotate_points_PCA(centred_x, centred_y, centred_z)

    def centre_points_centroid(
        self,
        raw_x: np.ndarray,
        raw_y: np.ndarray,
        raw_z: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        x = raw_x - raw_x.mean()
        y = raw_y - raw_y.mean()
        z = raw_z - raw_z.mean()
        return x, y, z

    def rotate_points_PCA(
        self,
        raw_x: np.ndarray,
        raw_y: np.ndarray,
        raw_z: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        positions = np.hstack([raw_x, raw_y, raw_z])

        pca = PCA(n_components=3)
        pca.fit(positions)

        rotation = np.array(pca.components_).T
        new_positions = rotation.dot(positions.T).T

        return (
            new_positions[:, 0].reshape(-1, 1),
            new_positions[:, 1].reshape(-1, 1),
            new_positions[:, 2].reshape(-1, 1),
        )
