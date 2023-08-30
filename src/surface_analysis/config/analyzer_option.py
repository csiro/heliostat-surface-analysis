from enum import Enum
from typing import Union, Optional
import typing

from pydantic import BaseModel, Field


class AnalyzerOptionName(Enum):
    basic = "basic"
    fit_surface = "fit_surface"
    known_focal = "known_focal"


class AnalyzerOption(BaseModel):
    name: AnalyzerOptionName
    params: Optional[typing.Dict[str, Union[str, float]]]
