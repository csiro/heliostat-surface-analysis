from heliostat_surface_analysis.linear_function.linear_function import LinearFunction


class FixedParaboloid(LinearFunction):
    def __init__(self):
        self.formula = "z = a(x^2 + y^2)"
        self.terms = [
            lambda x, y: x**2 + y**2,
        ]
        self.df_dx_terms = [
            lambda x, y: 2 * x,
        ]
        self.df_dy_terms = [
            lambda x, y: 2 * y,
        ]
