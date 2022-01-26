import pytest
from fastapi import APIRouter, FastAPI

from fastapi_crudrouter import (
    GinoCRUDRouter,
    MemoryCRUDRouter,
    OrmarCRUDRouter,
    SQLAlchemyCRUDRouter,
    DatabasesCRUDRouter,
)

# noinspection PyProtectedMember
from fastapi_crudrouter.core._base import CRUDGenerator
from tests import Potato


def test_router_type():
    assert issubclass(CRUDGenerator, APIRouter)
    assert issubclass(SQLAlchemyCRUDRouter, APIRouter)
    assert issubclass(MemoryCRUDRouter, APIRouter)
    assert issubclass(OrmarCRUDRouter, APIRouter)
    assert issubclass(GinoCRUDRouter, APIRouter)
    assert issubclass(DatabasesCRUDRouter, APIRouter)


def test_raise_not_implemented():
    app = FastAPI()

    def foo(*args, **kwargs):
        def bar():
            pass

        return bar

    methods = CRUDGenerator.get_routes()

    for m in methods:
        with pytest.raises(NotImplementedError):
            app.include_router(CRUDGenerator(schema=Potato))

        setattr(CRUDGenerator, f"_{m}", foo)

    app.include_router(CRUDGenerator(schema=Potato))
