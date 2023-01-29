import sys

from .databases_ import (
    databases_implementation,
    databases_implementation_custom_ids,
    databases_implementation_string_pk,
)
from .gino_ import (
    gino_implementation,
    gino_implementation_custom_ids,
    gino_implementation_integrity_errors,
    gino_implementation_string_pk,
)
from .memory import memory_implementation
from .ormar_ import (
    ormar_implementation,
    ormar_implementation_custom_ids,
    ormar_implementation_integrity_errors,
    ormar_implementation_string_pk,
)
from .sqlalchemy_ import (
    sqlalchemy_implementation,
    sqlalchemy_implementation_custom_ids,
    sqlalchemy_implementation_integrity_errors,
    sqlalchemy_implementation_string_pk,
    DSN_LIST,
)
from .tortoise_ import tortoise_implementation

implementations = [
    (memory_implementation, ""),
    (ormar_implementation, ""),
    (gino_implementation, ""),
]

implementations.extend([(sqlalchemy_implementation, dsn) for dsn in DSN_LIST])
implementations.extend([(databases_implementation, dsn) for dsn in DSN_LIST])


if sys.version_info >= (3, 8):
    implementations.append((tortoise_implementation, ""))
