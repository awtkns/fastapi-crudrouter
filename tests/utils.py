from fastapi import FastAPI

from tests.implementations import BaseImpl


def create_base_impl_with_overrides(impl: BaseImpl, **kwargs) -> FastAPI:
    settings = [{**s, **kwargs} for s in impl.get_settings()]
    return impl.create(settings=settings)


def compare_dict(d1, d2, exclude: list) -> bool:
    exclude = exclude or ["id"]
    d1 = {k: v for k, v in d1.items() if k not in exclude}
    d2 = {k: v for k, v in d2.items() if k not in exclude}
    return d1 == d2
