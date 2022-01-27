from abc import ABC
from typing import Type

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


@pytest.fixture(
    params=[
        GinoCRUDRouter,
        SQLAlchemyCRUDRouter,
        MemoryCRUDRouter,
        OrmarCRUDRouter,
        GinoCRUDRouter,
        DatabasesCRUDRouter,
    ]
)
def subclass(request) -> Type[CRUDGenerator]:
    return request.param


def test_router_is_subclass_of_crud_generator(subclass):
    assert issubclass(subclass, CRUDGenerator)


def test_router_is_subclass_of_api_router(subclass):
    assert issubclass(subclass, APIRouter)


def test_base_class_is_abstract():
    assert issubclass(CRUDGenerator, ABC)


def test_raise_not_implemented():
    app = FastAPI()

    def foo(*args, **kwargs):
        def bar():
            pass

        return bar

    methods = CRUDGenerator.get_routes()

    for m in methods:
        with pytest.raises(TypeError):
            app.include_router(CRUDGenerator(schema=Potato))

        setattr(CRUDGenerator, f"_{m}", foo)
