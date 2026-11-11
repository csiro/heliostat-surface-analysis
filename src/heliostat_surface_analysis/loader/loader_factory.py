from heliostat_surface_analysis.config.loader_option import LoaderOption
from heliostat_surface_analysis.config.loader_option import LoaderOptionName
from heliostat_surface_analysis.loader.txt_loader import TXTLoader
from heliostat_surface_analysis.loader.csv_loader import CSVLoader

class LoaderFactory:
    @classmethod
    def get_loader(cls, option: LoaderOption):
        if option.name == LoaderOptionName.txt:
            return TXTLoader(option.params)
        elif option.name == LoaderOptionName.csv:
            return CSVLoader(option.params)
        else:
            raise RuntimeError("loader: %s not recognised"%option.name)
