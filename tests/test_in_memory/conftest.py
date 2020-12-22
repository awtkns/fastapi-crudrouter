import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient

from fastapi_crudrouter import MemoryCRUDRouter as CRUDRouter

from . import Potato


@pytest.fixture
def client():
    app = FastAPI()

    app.include_router(CRUDRouter(model=Potato))

    yield TestClient(app)




