from enum import Enum
from typing import Optional

from pydantic import BaseModel


class LoaderOption(Enum):
    default = "default"
    leica = "leica"
    scaling = "scaling"


class PreprocessorOption(Enum):
    no = "no"
    basic = "basic"
    outlier = "outlier"


class AnalysisOption(Enum):
    basic = "basic"


class Config(BaseModel):
    width: float
    height: float
    loader: Optional[LoaderOption]
    preprocessor: Optional[PreprocessorOption]
    analysis: Optional[AnalysisOption]
