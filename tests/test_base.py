import pytest

from fastapi import FastAPI, APIRouter
from fastapi_crudrouter.core._base import CRUDGenerator
from fastapi_crudrouter import SQLAlchemyCRUDRouter, MemoryCRUDRouter

from tests import Potato, Carrot
from .implementations import memory_implementation


def test_router_type():
    assert issubclass(CRUDGenerator, APIRouter)
    assert issubclass(SQLAlchemyCRUDRouter, APIRouter)
    assert issubclass(MemoryCRUDRouter, APIRouter)


def test_get_one():
    app = FastAPI()

    def foo(*args, **kwargs):
        def bar():
            pass
        return bar

    foo()()

    methods = CRUDGenerator.get_routes()

    for m in methods:
        with pytest.raises(NotImplementedError):
            app.include_router(CRUDGenerator(model=Potato))

        setattr(CRUDGenerator, m, foo)

    app.include_router(CRUDGenerator(model=Potato))

