from enum import Enum
from typing import Union, Optional

from pydantic import BaseModel


class PreprocessorOptionName(Enum):
    no = "no"
    basic = "basic"
    known_size = "known_size"
    outlier = "outlier"


class PreprocessorOption(BaseModel):
    name: PreprocessorOptionName
    params: Optional[dict[str, Union[str, float]]]
