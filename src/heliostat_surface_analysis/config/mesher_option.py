from enum import Enum
from typing import Union, Optional
import typing

from pydantic import BaseModel


class MesherOptionName(Enum):
    Delaunay = "Delaunay"
    BSpline = "B-spline"


class MesherOption(BaseModel):
    name: MesherOptionName
    params: Optional[typing.Dict[str, Union[str, float]]]
