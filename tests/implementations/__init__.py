from .memory import memory_implementation
from .sqlalchemy_ import sqlalchemy_implementation, sqlalchemy_implementation_custom_ids
from .overloaded import overloaded_app
from .databases_ import databases_implementation, databases_implementation_custom_ids

implementations = [
    memory_implementation,
    sqlalchemy_implementation,
    databases_implementation
]

try:
    from .tortoise_ import tortoise_implementation
except ImportError:
    pass
else:
    implementations.append(tortoise_implementation)
