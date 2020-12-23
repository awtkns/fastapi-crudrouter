import pytest
from fastapi.testclient import TestClient

from .implementations import memory_implementation, sqlalchemy_implementation


@pytest.fixture(params=[memory_implementation, sqlalchemy_implementation])
def client(request):

    yield TestClient(request.param())




