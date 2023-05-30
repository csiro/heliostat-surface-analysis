from enum import Enum
from typing import Union, Optional

from pydantic import BaseModel


class LoaderOptionName(Enum):
    default = "default"
    csv_loader = "csv_loader"
    scaling = "scaling"
    leica = "leica"


class LoaderOption(BaseModel):
    name: LoaderOptionName
    params: Optional[dict[str, Union[str, float]]]
