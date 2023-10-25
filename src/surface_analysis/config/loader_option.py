from enum import Enum
from typing import Union, Optional
import typing

from pydantic import BaseModel


class LoaderOptionName(Enum):
    default = "default"
    csv = "csv"
    scaling = "scaling"
    leica = "leica"


class LoaderOption(BaseModel):
    name: LoaderOptionName
    params: Optional[typing.Dict[str, Union[str, float]]]
