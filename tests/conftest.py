from typing import Type

import pytest


import inspect
from fastapi.testclient import TestClient

from .implementations import *
from .implementations._base import BaseImpl, TestCase

from tests import config


def yield_test_client(app, impl):
    # if impl.__name__ == "tortoise_implementation":
    #     from tortoise.contrib.test import initializer, finalizer
    #
    #     initializer(["tests.implementations.tortoise_"])
    #     with TestClient(app) as c:
    #         yield c
    #     finalizer()
    #
    # else:
    with TestClient(app) as c:
        yield c


def label_func(*args):
    impl = args[0]
    return str(impl)


@pytest.fixture(params=implementations, ids=label_func, scope="class")
def client(request):
    impl: BaseImpl = request.param

    impl.datasource.clean()
    app = impl.create(TestCase.DEFAULT)

    yield from yield_test_client(app, impl)


@pytest.fixture(params=[])
def custom_id_client(request):
    yield from yield_test_client(request.param(), request.param)


@pytest.fixture(
    params=[],
    scope="function",
)
def string_pk_client(request):
    yield from yield_test_client(request.param(), request.param)


@pytest.fixture(
    params=[],
    scope="function",
)
def integrity_errors_client(request):
    yield from yield_test_client(request.param(), request.param)
