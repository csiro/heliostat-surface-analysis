from heliostat_surface_analysis.config.mesher_option import MesherOption
from heliostat_surface_analysis.config.mesher_option import MesherOptionName
from heliostat_surface_analysis.mesher.delaunay_mesher import DelaunayMesher
from heliostat_surface_analysis.mesher.bspline_mesher import BSplineMesher

class MesherFactory:
    @classmethod
    def get_mesher(cls, option: MesherOption):
        if option.name == MesherOptionName.Delaunay:
            return DelaunayMesher(option.params)
        elif option.name == MesherOptionName.BSpline:
            return BSplineMesher(option.params)
        else:
            raise RuntimeError("mesher: %s not recognised"%option.name)
