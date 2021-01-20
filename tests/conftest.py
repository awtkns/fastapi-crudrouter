import pytest
from fastapi.testclient import TestClient

from .implementations import *

implementations = [
    memory_implementation,
    sqlalchemy_implementation,
    databases_implementation
]


@pytest.fixture(params=implementations)
def client(request):

    yield TestClient(request.param())


@pytest.fixture(params=[sqlalchemy_implementation_custom_ids, databases_implementation_custom_ids])
def custom_id_client(request):

    yield TestClient(request.param())


@pytest.fixture
def overloaded_client():

    yield TestClient(overloaded_app())


@pytest.fixture(params=[sqlalchemy_implementation_string_pk, databases_implementation_string_pk], scope='function')
def string_pk_client(request):

    yield TestClient(request.param())
