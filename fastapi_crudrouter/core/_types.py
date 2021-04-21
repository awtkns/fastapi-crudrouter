from typing import Dict, TypeVar, Optional, Sequence, Union

from fastapi.params import Depends
from pydantic import BaseModel

PAGINATION = Dict[str, Optional[int]]
FILTER = Dict[str, Optional[Union[int, float, str, bool]]]
PYDANTIC_SCHEMA = BaseModel

T = TypeVar("T", bound=BaseModel)
DEPENDENCIES = Optional[Sequence[Depends]]
