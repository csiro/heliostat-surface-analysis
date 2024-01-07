from heliostat_surface_analysis.linear_function.linear_function import LinearFunction


class Plane(LinearFunction):
    def __init__(self):
        self.formula = "z = bx + cy + d"
        self.terms = [
            lambda x, y: x,
            lambda x, y: y,
            lambda x, y: x * 0 + 1,
        ]
        self.df_dx_terms = [
            lambda x, y: 0 * x + 1,
            lambda x, y: 0 * x,
            lambda x, y: 0 * x,
        ]
        self.df_dy_terms = [
            lambda x, y: 0 * x,
            lambda x, y: 0 * x + 1,
            lambda x, y: 0 * x,
        ]
