import pytest
from fastapi.testclient import TestClient

try:
    from tortoise.contrib.test import initializer, finalizer
except ImportError:
    pass

from .implementations import *


@pytest.fixture(params=implementations)
def client(request):
    impl = request.param

    if impl.__name__ is 'tortoise_implementation':
        initializer(["tests.implementations.tortoise_"])
        with TestClient(impl()) as c:
            yield c
        finalizer()

    else:
        yield TestClient(impl())


@pytest.fixture(params=[sqlalchemy_implementation_custom_ids, databases_implementation_custom_ids])
def custom_id_client(request):

    yield TestClient(request.param())


@pytest.fixture
def overloaded_client():

    yield TestClient(overloaded_app())




