import numpy as np
import typing

from surface_analysis.preprocessor.basic_preprocessor import BasicPreprocessor
from surface_analysis.mesh.leica_mesher import points_to_tris, points_and_tris_to_mesh
from surface_analysis.vector_math import normalise_vectors


MIN_ANGLE_THRESHOLD = 0.1


class OutlierPreprocessor(BasicPreprocessor):
    def preprocess_points(
        self,
        raw_x: np.ndarray,
        raw_y: np.ndarray,
        raw_z: np.ndarray,
    ) -> typing.Tuple[np.ndarray, np.ndarray, np.ndarray]:
        x, y, z = super().preprocess_points(raw_x, raw_y, raw_z)
        trimmed_x, trimmed_y, trimmed_z = self.remove_outliers(x, y, z)
        return super().preprocess_points(raw_x, raw_y, raw_z)

    def remove_outliers(
        self,
        x: np.ndarray,
        y: np.ndarray,
        z: np.ndarray,
    ) -> typing.Tuple[np.ndarray, np.ndarray, np.ndarray]:
        tris = points_to_tris(x, y)
        mesh = points_and_tris_to_mesh(x, y, z, tris)

        unit_normals = normalise_vectors(mesh.normals)
        # Dot product with z axis is just the z component
        z_components = unit_normals[:, 2]
        z_components = np.clip(z_components, -1, 1)
        angles = np.arccos(z_components)

        vertex_min_angles = {}
        for i in range(tris.simplices.shape[0]):
            angle = angles[i]
            for j in range(tris.simplices.shape[1]):
                vertex = tris.simplices[i, j]
                if vertex in vertex_min_angles:
                    if angle < vertex_min_angles[vertex]:
                        vertex_min_angles[vertex] = angle
                else:
                    vertex_min_angles[vertex] = angle

        vertices_to_delete = []
        for vertex, min_angle in vertex_min_angles.items():
            if min_angle > MIN_ANGLE_THRESHOLD:
                vertices_to_delete.append(vertex)

        x = np.delete(x, vertices_to_delete, axis=0)
        y = np.delete(y, vertices_to_delete, axis=0)
        z = np.delete(z, vertices_to_delete, axis=0)

        return x, y, z
