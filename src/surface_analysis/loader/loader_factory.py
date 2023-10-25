from surface_analysis.config.loader_option import LoaderOption
from surface_analysis.config.loader_option import LoaderOptionName
from surface_analysis.loader.default_loader import DefaultLoader
from surface_analysis.loader.csv_loader import CSVLoader
from surface_analysis.loader.leica_loader import LeicaLoader
from surface_analysis.loader.scaling_loader import ScalingLoader


class LoaderFactory:
    @classmethod
    def get_loader(cls, option: LoaderOption):
        if option.name == LoaderOptionName.default:
            return DefaultLoader()
        elif option.name == LoaderOptionName.csv:
            return CSVLoader()
        elif option.name == LoaderOptionName.leica:
            return LeicaLoader()
        elif option.name == LoaderOptionName.scaling:
            return ScalingLoader(option.params)
        else:
            return DefaultLoader()
