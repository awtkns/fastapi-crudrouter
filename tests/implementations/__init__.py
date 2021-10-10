from tests.conf import datasource_factory
from ._base import BaseImpl, TestCase
from .databases_ import DatabasesImpl
from .gino_ import GinoImpl
from .memory import MemoryImpl
from .ormar_ import OrmarImpl
from .sqlalchemy_ import SqlAlchemyImpl

_implementations = [
    MemoryImpl,
    SqlAlchemyImpl,
    OrmarImpl,
    GinoImpl,
    DatabasesImpl,
]

try:
    from .tortoise_ import TortoiseImpl
except ImportError:
    TortoiseImpl = None
else:
    _implementations.append(TortoiseImpl)


implementations = []
for cls in _implementations:
    for uri in cls.__backends__:
        ds = datasource_factory.get_datasource(uri)
        implementations.append(cls(ds))
