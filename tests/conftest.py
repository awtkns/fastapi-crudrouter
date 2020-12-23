import pytest
from fastapi.testclient import TestClient

from .implementations import memory_implementation, sqlalchemy_implementation, overloaded_app


@pytest.fixture(params=[memory_implementation, sqlalchemy_implementation])
def client(request):

    yield TestClient(request.param())


@pytest.fixture
def overloaded_client():

    yield TestClient(overloaded_app())


