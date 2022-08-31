

class MirrorSurface:
    def __init__(self, points: str, mesh: float, facets: str):
        self.mirror_name = mirror_name
        self.design_focal_length = design_focal_length
        self.file_path = file_path
        self.points = self.load_points(file_path)
        self.mesh = self.create_mesh(self.points)
        self.facets = self.create_facets(self.mesh)

    def load_points(self, file_path: str) -> pd.DataFrame:
        points = pd.read_csv(
            file_path,
            skiprows=7,
            delimiter=",  ",
            header=None,
            engine="python",
        )
        points = self.cleanup_columns(points)
        points = self.scale_mm_to_m(points)
        return self.centre_and_rotate_points(points)

    def scale_mm_to_m(self, points):
        points = points.copy()
        points /= 1000
        return points

    def cleanup_columns(self, points):
        points = points.copy()
        columns_to_drop = list(range(4, 6)) + list(range(9, len(points.columns)))
        points.drop(
            points.columns[columns_to_drop],
            axis=1,
            inplace=True,
        )
        points.columns = [
            "index",
            "x",
            "y",
            "z",
            "del_x",
            "del_y",
            "del_z",
        ]
        points = points.set_index("index")
        return points

    def centre_and_rotate_points(self, points: pd.DataFrame) -> pd.DataFrame:
        points["x"] -= points["x"].mean()
        points["y"] -= points["y"].mean()
        points["z"] -= points["z"].mean()

        positions = np.array(points[["x", "y", "z"]], copy=True)
        uncertainties = np.array(points[["del_x", "del_y", "del_z"]], copy=True)

        pca = PCA(n_components=3)
        pca.fit(positions)

        rotation = np.array(pca.components_).T
        new_positions = rotation.dot(positions.T).T
        new_uncertainties = rotation.dot(uncertainties.T).T

        points["x"] = new_positions[:, 0]
        points["y"] = new_positions[:, 1]
        points["z"] = new_positions[:, 2]
        points["del_x"] = new_uncertainties[:, 0]
        points["del_y"] = new_uncertainties[:, 1]
        points["del_z"] = new_uncertainties[:, 2]

        return points

    def create_mesh(self, data: pd.DataFrame) -> mesh.Mesh:
        xy_points = data[["x", "y"]].to_numpy()
        xyz_points = data[["x", "y", "z"]].to_numpy()
        self.triangles = Delaunay(xy_points)

        small_triangles = []
        for i, triangle in enumerate(self.triangles.simplices):
            a, b, c = triangle
            ab = np.sqrt((self.triangles.points[a][0] - self.triangles.points[b][0])**2 + (self.triangles.points[a][1] - self.triangles.points[b][1])**2)
            bc = np.sqrt((self.triangles.points[b][0] - self.triangles.points[c][0])**2 + (self.triangles.points[b][1] - self.triangles.points[c][1])**2)
            ca = np.sqrt((self.triangles.points[c][0] - self.triangles.points[a][0])**2 + (self.triangles.points[c][1] - self.triangles.points[a][1])**2)
            if np.all(np.array([ab, bc, ca]) < MAX_EDGE_LENGTH):
                small_triangles.append(triangle)

        self.triangles.simplices = np.array(small_triangles)


        surface_mesh = mesh.Mesh(
            np.zeros(self.triangles.simplices.shape[0], dtype=mesh.Mesh.dtype)
        )
        for i, simplex in enumerate(self.triangles.simplices):
            for j in range(3):
                surface_mesh.vectors[i][j] = xyz_points[simplex[j], :]

        surface_mesh.update_normals()

        return surface_mesh

    def create_facets(self, mesh_data: mesh.Mesh) -> pd.DataFrame:
        facets = pd.DataFrame(
            data=mesh_data.points,
            dtype=float,
            columns=["x1", "y1", "z1", "x2", "y2", "z2", "x3", "y3", "z3"],
        )
        facets["x"] = (facets["x1"] + facets["x2"] + facets["x3"]) / 3.0
        facets["y"] = (facets["y1"] + facets["y2"] + facets["y3"]) / 3.0
        facets["z"] = (facets["z1"] + facets["z2"] + facets["z3"]) / 3.0
        facets["r"] = np.sqrt(facets["x"] ** 2 + facets["y"] ** 2)

        normals = pd.DataFrame(
            mesh_data.normals,
            dtype=float,
            columns=["x", "y", "z"],
        )

        normals["mag"] = np.linalg.norm(normals, axis=1)
        facets["normal"] = normals.apply(
            lambda row: [row["x"], row["y"], row["z"]] / row["mag"],
            axis=1,
        )

        return facets
