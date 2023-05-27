from typing import Optional

from surface_analysis.config.config import LoaderOption
from surface_analysis.loader.default_loader import DefaultLoader
from surface_analysis.loader.leica_loader import LeicaLoader
from surface_analysis.loader.scaling_loader import ScalingLoader

class LoaderFactory:
    @classmethod
    def get_loader(cls, option: Optional[LoaderOption]):
        if option == LoaderOption.default:
            return DefaultLoader()
        elif option == LoaderOption.leica:
            return LeicaLoader()
        elif option == LoaderOption.scaling:
            return ScalingLoader()
        else:
            return DefaultLoader()
