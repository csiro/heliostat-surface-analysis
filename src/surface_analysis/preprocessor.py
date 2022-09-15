import numpy as np
from sklearn.decomposition import PCA


def centre_points_centroid(
    raw_x: np.ndarray,
    raw_y: np.ndarray,
    raw_z: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray,]:
    x = raw_x - raw_x.mean()
    y = raw_y - raw_y.mean()
    z = raw_z - raw_z.mean()
    return (x, y, z)


def rotate_points_PCA(
    raw_x: np.ndarray,
    raw_y: np.ndarray,
    raw_z: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray,]:
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
