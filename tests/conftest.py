import pytest
from fastapi.testclient import TestClient

from .implementations import *


@pytest.fixture(params=[memory_implementation, sqlalchemy_implementation])
def client(request):

    yield TestClient(request.param())


@pytest.fixture
def overloaded_client():

    yield TestClient(overloaded_app())


@pytest.fixture
def custom_id_client():

    yield TestClient(sqlalchemy_implementation_custom_ids())


