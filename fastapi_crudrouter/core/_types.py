from typing import Dict, Optional, TypeVar, Coroutine, Callable, Any, Type

from pydantic import BaseModel

PAGINATION = Dict[str, Optional[int]]
PYDANTIC_SCHEMA = BaseModel

T = TypeVar("T", bound=BaseModel)
