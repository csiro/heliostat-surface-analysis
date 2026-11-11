from enum import Enum
from typing import Union, Optional
import typing

from pydantic import BaseModel, Field


class AnalyserOptionName(Enum):
    basic = "basic"
    fit_surface = "fit_surface"
    fixed_focal_length = "fixed_focal_length"


class AnalyserOption(BaseModel):
    name: AnalyserOptionName
    params: Optional[typing.Dict[str, Union[str, float]]]
