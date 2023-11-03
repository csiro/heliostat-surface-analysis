from enum import Enum
from typing import Union, Optional
import typing

from pydantic import BaseModel


class PreprocessorOptionName(Enum):
    none = "none"
    basic = "basic"
    fixed_focal_length = "fixed_focal_length"
    outlier = "outlier"


class PreprocessorOption(BaseModel):
    name: PreprocessorOptionName
    params: Optional[typing.Dict[str, Union[str, float]]]
