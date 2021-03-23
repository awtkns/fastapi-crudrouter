from .databases_ import (
    databases_implementation,
    databases_implementation_custom_ids,
    databases_implementation_string_pk,
)
from .memory import memory_implementation
from .overloaded import overloaded_app
from .sqlalchemy_ import (
    sqlalchemy_implementation,
    sqlalchemy_implementation_custom_ids,
    sqlalchemy_implementation_string_pk,
)

implementations = [
    memory_implementation,
    sqlalchemy_implementation,
    databases_implementation,
]

try:
    from .tortoise_ import tortoise_implementation
except ImportError:
    pass
else:
    implementations.append(tortoise_implementation)

try:
    from .ormar_ import (
        ormar_implementation,
        ormar_implementation_string_pk,
        ormar_implementation_custom_ids,
    )
except ImportError:
    pass
else:
    implementations.append(ormar_implementation)
