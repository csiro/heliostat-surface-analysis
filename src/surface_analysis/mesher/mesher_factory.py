from surface_analysis.config.mesher_option import MesherOption
from surface_analysis.config.mesher_option import MesherOptionName
from surface_analysis.mesher.delaunay_mesher import DelaunayMesher


class MesherFactory:
    @classmethod
    def get_mesher(cls, option: MesherOption):
        if option.name == MesherOptionName.Delaunay:
            return DelaunayMesher(option.params)
        else:
            raise RuntimeError("mesher: %s not recognised"%option.name)
