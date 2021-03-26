import pytest
from fastapi.testclient import TestClient

from .implementations import *


@pytest.fixture(params=implementations, scope="class")
def client(request):
    impl = request.param

    if impl.__name__ == "tortoise_implementation":
        from tortoise.contrib.test import initializer, finalizer

        initializer(["tests.implementations.tortoise_"])
        with TestClient(impl()) as c:
            yield c
        finalizer()

    else:
        with TestClient(impl()) as c:
            yield c


@pytest.fixture(
    params=[
        sqlalchemy_implementation_custom_ids,
        databases_implementation_custom_ids,
        ormar_implementation_custom_ids,
    ]
)
def custom_id_client(request):
    with TestClient(request.param()) as c:
        yield c


@pytest.fixture
def overloaded_client():
    yield TestClient(overloaded_app())


@pytest.fixture(
    params=[
        sqlalchemy_implementation_string_pk,
        databases_implementation_string_pk,
        ormar_implementation_string_pk,
    ],
    scope="function",
)
def string_pk_client(request):
    with TestClient(request.param()) as c:
        yield c


@pytest.fixture(
    params=[
        sqlalchemy_implementation_integrity_errors,
        ormar_implementation_integrity_errors,
    ],
    scope="function",
)
def integrity_errors_client(request):
    with TestClient(request.param()) as c:
        yield c
