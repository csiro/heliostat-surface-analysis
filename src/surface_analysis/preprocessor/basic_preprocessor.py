import numpy as np
from sklearn.decomposition import PCA

from surface_analysis.preprocessor.preprocessor import Preprocessor


class BasicPreprocessor(Preprocessor):
    def preprocess_points(
        self,
        raw_x: np.ndarray,
        raw_y: np.ndarray,
        raw_z: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        centred_x, centred_y, centred_z = self.centre_points_centroid(raw_x, raw_y, raw_z)
        rotated_x, rotated_y, rotated_z = self.rotate_points_PCA(centred_x, centred_y, centred_z)
        return self.rotate_xy_plane(rotated_x, rotated_y, rotated_z)

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

    def rotate_xy_plane(
        self,
        raw_x: np.ndarray,
        raw_y: np.ndarray,
        raw_z: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        points = np.hstack((raw_x, raw_y, raw_z)).T

        best_theta = 0
        best_area = 999
        steps = 200
        for theta in np.arange(0, np.pi, np.pi / steps):
            rot = np.array(
                [[np.cos(theta), -np.sin(theta), 0],
                [np.sin(theta), np.cos(theta), 0],
                [0, 0, 1]]
            )
            rotated_points = rot @ points

            max_x = np.max(np.absolute(rotated_points[0,:]))
            max_y = np.max(np.absolute(rotated_points[1,:]))

            if max_x * max_y < best_area:
                best_area = max_x * max_y
                best_theta = theta

        rot = np.array(
            [[np.cos(best_theta), -np.sin(best_theta), 0],
            [np.sin(best_theta), np.cos(best_theta), 0],
            [0, 0, 1]]
        )
        rotated_points = rot @ points

        return (
            rotated_points[:,0],
            raw_y,
            raw_z
        )
