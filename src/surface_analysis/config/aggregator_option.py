from enum import Enum
from typing import Union, Optional
import typing

from pydantic import BaseModel, Field

class AggregatorOptionName(Enum):
    sum = "sum"
    squared_sum = "squared_sum"
    mean = "mean"
    rms = "rms"
    mode = "mode"
    weighted_sum = "weighted_sum"
    weighted_squared_sum = "weighted_squared_sum"
    weighted_mean = "weighted_mean"
    weighted_rms = "weighted_rms"
    weighted_mode = "weighted_mode"

class AggregatorOption(BaseModel):
    name: AggregatorOptionName
    params: Optional[typing.Dict[str, Union[str, float]]]
