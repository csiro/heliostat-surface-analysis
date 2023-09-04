import numpy as np
from sklearn.decomposition import PCA
import typing

from surface_analysis.preprocessor.preprocessor import Preprocessor


class BasicPreprocessor(Preprocessor):
    def preprocess_points(
        self,
        raw_x: np.ndarray,
        raw_y: np.ndarray,
        raw_z: np.ndarray,
    ) -> typing.Tuple[np.ndarray, np.ndarray, np.ndarray]:
        centred_x, centred_y, centred_z = self.centre_points_centroid(raw_x, raw_y, raw_z)
        return self.rotate_points_PCA(centred_x, centred_y, centred_z)

    def centre_points_centroid(
        self,
        raw_x: np.ndarray,
        raw_y: np.ndarray,
        raw_z: np.ndarray,
    ) -> typing.Tuple[np.ndarray, np.ndarray, np.ndarray]:
               
        x = raw_x - raw_x.mean()
        y = raw_y - raw_y.mean()
        z = raw_z - raw_z.mean()
        
        return x, y, z

    # FIXME: this results in rotation about the z axis that we don't want as this is already correct in original data
    def rotate_points_PCA(
        self,
        raw_x: np.ndarray,
        raw_y: np.ndarray,
        raw_z: np.ndarray,
    ) -> typing.Tuple[np.ndarray, np.ndarray, np.ndarray]:
        positions = np.hstack([raw_x, raw_y, raw_z])

        pca = PCA(n_components=3)
        pca.fit(positions)

        rotation = np.array(pca.components_).T
        new_positions = rotation.dot(positions.T).T
        
        if 0:
            # reverse the z rotation that was applied in the above transformation
            # FIXME: doesn't always work
            r11, r12, r13 = rotation[0]
            r21, r22, r23 = rotation[1]
            r31, r32, r33 = rotation[2]
            theta1 = np.arctan(-r23 / r33)
            theta2 = np.arctan(r13 * np.cos(theta1) / r33)
            theta3 = np.arctan2(-r12 , r11)
            print("theta1 = ",(theta1*180/np.pi))
            print("theta2 = ",(theta2*180/np.pi))
            print("theta3 = ",(theta3*180/np.pi))
            zrot = np.array(
                    [[np.cos(-theta3), -np.sin(-theta3), 0],
                    [np.sin(-theta3), np.cos(-theta3), 0],
                    [0, 0, 1]],
                    dtype=np.float64
                )
            corrected_positions = zrot.dot(new_positions.T).T
            
            return (
                corrected_positions[:, 0].reshape(-1, 1),
                corrected_positions[:, 1].reshape(-1, 1),
                corrected_positions[:, 2].reshape(-1, 1),
            )
        else:
            return (
                new_positions[:, 0].reshape(-1, 1),
                new_positions[:, 1].reshape(-1, 1),
                new_positions[:, 2].reshape(-1, 1),
            )
