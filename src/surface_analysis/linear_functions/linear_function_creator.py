from surface_analysis.linear_functions.linear_function import LinearFunction


class LinearFunctionCreator:
    def centred_circular_paraboloid(self) -> LinearFunction:
        name = "centred_circular_paraboloid"
        formula = "z = a(x^2 + y^2)"
        terms = [
            lambda x, y: x**2 + y**2,
        ]
        df_dx_terms = [
            lambda x, y: 2 * x,
        ]
        df_dy_terms = [
            lambda x, y: 2 * y,
        ]
        return LinearFunction(name, formula, terms, df_dx_terms, df_dy_terms)

    def centred_circular_paraboloid_with_z_offset(self) -> LinearFunction:
        name = "centred_circular_paraboloid_with_z_offset"
        formula = "z = a(x^2 + y^2) + b"
        terms = [
            lambda x, y: x**2 + y**2,
            lambda x, y: x * 0 + 1,
        ]
        df_dx_terms = [
            lambda x, y: 2 * x,
            lambda x, y: 0 * x,
        ]
        df_dy_terms = [
            lambda x, y: 2 * y,
            lambda x, y: 0 * x,
        ]
        return LinearFunction(name, formula, terms, df_dx_terms, df_dy_terms)


    def circular_paraboloid(self) -> LinearFunction:
        name = "circular_paraboloid"
        formula = "z = a(x^2 + y^2) + bx + cy + d"
        terms = [
            lambda x, y: x**2 + y**2,
            lambda x, y: x,
            lambda x, y: y,
            lambda x, y: x * 0 + 1,
        ]
        df_dx_terms = [
            lambda x, y: 2 * x,
            lambda x, y: 0 * x + 1,
            lambda x, y: 0 * x,
            lambda x, y: 0 * x,
        ]
        df_dy_terms = [
            lambda x, y: 2 * y,
            lambda x, y: 0 * x,
            lambda x, y: 0 * x + 1,
            lambda x, y: 0 * x,
        ]
        return LinearFunction(name, formula, terms, df_dx_terms, df_dy_terms)


    def elliptic_paraboloid(self) -> LinearFunction:
        name = "elliptic_paraboloid"
        formula = "z = ax^2 + bx + cy^2 + dy + e"
        terms = [
            lambda x, y: x**2,
            lambda x, y: x,
            lambda x, y: y**2,
            lambda x, y: y,
            lambda x, y: x * 0 + 1,
        ]
        df_dx_terms = [
            lambda x, y: 2 * x,
            lambda x, y: 0 * x + 1,
            lambda x, y: 0 * x,
            lambda x, y: 0 * x,
            lambda x, y: 0 * x,
        ]
        df_dy_terms = [
            lambda x, y: 0 * x,
            lambda x, y: 0 * x,
            lambda x, y: 2 * y,
            lambda x, y: 0 * x + 1,
            lambda x, y: 0 * x,
        ]
        return LinearFunction(name, formula, terms, df_dx_terms, df_dy_terms)

    def general_paraboloid(self) -> LinearFunction:
        name = "general_paraboloid"
        formula = "z = ax^2 + bx + cy^2 + dy + exy + f"
        terms = [
            lambda x, y: x**2,
            lambda x, y: x,
            lambda x, y: y**2,
            lambda x, y: y,
            lambda x, y: x * y,
            lambda x, y: x * 0 + 1,
        ]
        df_dx_terms = [
            lambda x, y: 2 * x,
            lambda x, y: 0 * x + 1,
            lambda x, y: 0 * x,
            lambda x, y: 0 * x,
            lambda x, y: y,
            lambda x, y: 0 * x,
        ]
        df_dy_terms = [
            lambda x, y: 0 * x,
            lambda x, y: 0 * x,
            lambda x, y: 2 * y,
            lambda x, y: 0 * x + 1,
            lambda x, y: x,
            lambda x, y: 0 * x,
        ]
        return LinearFunction(name, formula, terms, df_dx_terms, df_dy_terms)

    def high_order_poly(self) -> LinearFunction:
        name = "high_order_poly"
        formula = "ax^2*y^2 + bx^2*y + cx^2 + dxy^2 + exy + fx + gy^2 + hy + i"
        terms = [
            lambda x, y: x**2 * y**2,
            lambda x, y: x**2 * y,
            lambda x, y: x**2,
            lambda x, y: x * y**2,
            lambda x, y: x * y,
            lambda x, y: x,
            lambda x, y: y**2,
            lambda x, y: y,
            lambda x, y: x * 0 + 1,
        ]
        df_dx_terms = [
            lambda x, y: 2 * x * y**2,
            lambda x, y: 2 * x * y,
            lambda x, y: 2 * x,
            lambda x, y: y**2,
            lambda x, y: y,
            lambda x, y: 0 * x + 1,
            lambda x, y: 0 * x,
            lambda x, y: 0 * x,
            lambda x, y: 0 * x,
        ]
        df_dy_terms = [
            lambda x, y: 2 * y * x**2,
            lambda x, y: x**2,
            lambda x, y: 0 * x,
            lambda x, y: 2 * y * x,
            lambda x, y: x,
            lambda x, y: 0 * x,
            lambda x, y: 2 * y,
            lambda x, y: 0 * x + 1,
            lambda x, y: 0 * x,
        ]
        return LinearFunction(name, formula, terms, df_dx_terms, df_dy_terms)
