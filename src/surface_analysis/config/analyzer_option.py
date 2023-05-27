from enum import Enum
from typing import Union, Optional

from pydantic import BaseModel


class AnalyzerOptionName(Enum):
    basic = "basic"
    supplied_reference = "supplied_reference"


class AnalyzerOption(BaseModel):
    name: AnalyzerOptionName
    params: Optional[dict[str, Union[str, float]]]
