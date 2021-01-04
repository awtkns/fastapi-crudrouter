import random
import pytest

from fastapi import FastAPI, testclient, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi_crudrouter import MemoryCRUDRouter

from tests import Potato

URL = '/potato'
AUTH = {'Authorization': 'Bearer my_token'}


def get_client():
    app = FastAPI()
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

    def token_auth(token: str = Depends(oauth2_scheme)):
        print(token)
        if not token:
            raise HTTPException(401, "Invalid token")

    router = MemoryCRUDRouter(schema=Potato, dependencies=[Depends(token_auth)])
    app.include_router(router)

    return testclient.TestClient(app)


def test_authorization():
    client = get_client()

    assert client.get(URL, headers=AUTH).status_code == 200
    assert client.post(URL, headers=AUTH).status_code != 401
    assert client.delete(URL, headers=AUTH).status_code == 200


def test_authorization_fail():
    client = get_client()

    assert client.get(URL).status_code == 401
    assert client.get(URL).status_code == 401
    assert client.post(URL).status_code == 401

    for id_ in [-1, 1, 0, 14]:
        assert client.get(f'{URL}/{id_}').status_code == 401
        assert client.put(f'{URL}/{id_}').status_code == 401
        assert client.delete(f'{URL}/{id_}').status_code == 401
