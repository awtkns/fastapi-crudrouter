from tests.conf import datasource_factory

from .sqlalchemy_ import SqlAlchemyImpl

_implementations = [SqlAlchemyImpl]

implementations = []
for impl_cls in _implementations:
    for uri in impl_cls.supported_backends():
        ds = datasource_factory.get_datasource(uri)
        implementations.append(impl_cls(ds))
