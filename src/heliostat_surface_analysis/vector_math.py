import numpy as np


def normalise_vectors(vectors: np.ndarray) -> np.ndarray:
    """
    Takes an NxM array where each row is a vector to be scaled to length 1.
        v_hat = v / ||v||
    """
    vector_lengths = np.linalg.norm(vectors, axis=1, keepdims=True)
    return vectors / vector_lengths


def area_of_triangles(p0: np.ndarray, p1: np.ndarray, p2: np.ndarray) -> np.ndarray:
    """
    Cross product has magnitude equal to parallelogram area.
    Triangle area will be half that.
    """
    magnitude = np.linalg.norm(np.cross(p1 - p0, p2 - p0), axis=1, keepdims=True)
    return magnitude / 2


def area_of_triangles_xy(p0: np.ndarray, p1: np.ndarray, p2: np.ndarray) -> np.ndarray:
    """
    Get only the area of the projection of the triangle on the xy plane.
    Cross product has magnitude equal to parallelogram area.
    Triangle area will be half that.
    """
    p0 = p0.copy()
    p1 = p1.copy()
    p2 = p2.copy()
    p0[:, 2] = 0
    p1[:, 2] = 0
    p2[:, 2] = 0
    return area_of_triangles(p0, p1, p2)
