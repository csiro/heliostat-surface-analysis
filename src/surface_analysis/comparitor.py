import numpy as np

from surface_analysis.vector_math import normalise_vectors


def difference(
    z0: np.ndarray,
    z1: np.ndarray,
) -> np.ndarray:
    return z1 - z0


def angular_difference(
    measured_normals: np.ndarray,
    ideal_normals: np.ndarray,
) -> np.ndarray:
    measured_unit_normals = normalise_vectors(measured_normals)
    ideal_unit_normals = normalise_vectors(ideal_normals)

    measured_dot_ideal = np.sum(
        measured_unit_normals * ideal_unit_normals,
        axis=1,
        keepdims=True,
    )
    # Computational precision can result in values slightly outside [-1, 1]
    measured_dot_ideal = np.clip(measured_dot_ideal, -1, 1)

    return np.arccos(measured_dot_ideal)
