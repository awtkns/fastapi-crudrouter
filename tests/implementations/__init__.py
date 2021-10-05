from tests.conf import datasource_factory

from ._base import BaseImpl, TestCase
from .sqlalchemy_ import SqlAlchemyImpl

_implementations = [SqlAlchemyImpl]

implementations = []
for impl_cls in _implementations:
    for uri in impl_cls.__backends__:
        ds = datasource_factory.get_datasource(uri)
        implementations.append(impl_cls(ds))
