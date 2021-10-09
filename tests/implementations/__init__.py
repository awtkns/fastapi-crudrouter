from tests.conf import datasource_factory

from ._base import BaseImpl, TestCase
from .sqlalchemy_ import SqlAlchemyImpl
from .memory import MemoryImpl
from .ormar_ import OrmarImpl
from .gino_ import GinoImpl
from .databases_ import DatabasesImpl
from .tortoise_ import TortoiseImpl

implementations = []
for impl_cls in [
    MemoryImpl,
    SqlAlchemyImpl,
    OrmarImpl,
    GinoImpl,
    DatabasesImpl,
    TortoiseImpl,
]:
    for uri in impl_cls.__backends__:
        ds = datasource_factory.get_datasource(uri)
        implementations.append(impl_cls(ds))
