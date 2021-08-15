from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

import pytest

from tests.implementations import implementations
from tests.conftest import yield_test_client

URLS = ["/potato", "/carrot"]
AUTH = {"Authorization": "Bearer my_token"}


@pytest.fixture(params=implementations, scope="class")
def client(request):
    impl, dsn = request.param

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

    def token_auth(token: str = Depends(oauth2_scheme)):
        if not token:
            raise HTTPException(401, "Invalid token")

    app, router, settings = impl(db_uri=dsn)
    [
        app.include_router(router(**s, dependencies=[Depends(token_auth)]))
        for s in settings
    ]

    yield from yield_test_client(app, impl)


@pytest.fixture(params=URLS)
def url(request):
    yield request.param


class TestTopLevelDependencies:
    @staticmethod
    def test_authorization(client, url):
        assert client.get(url, headers=AUTH).status_code == 200
        assert client.post(url, headers=AUTH).status_code != 401
        assert client.delete(url, headers=AUTH).status_code == 200

        for id_ in [-1, 1, 0, 14]:
            assert client.get(f"{url}/{id_}", headers=AUTH).status_code != 401
            assert client.put(f"{url}/{id_}", headers=AUTH).status_code != 401
            assert client.delete(f"{url}/{id_}", headers=AUTH).status_code != 401

    @staticmethod
    def test_authorization_fail(client, url):
        assert client.get(url).status_code == 401
        assert client.get(url).status_code == 401
        assert client.post(url).status_code == 401

        for id_ in [-1, 1, 0, 14]:
            assert client.get(f"{url}/{id_}").status_code == 401
            assert client.put(f"{url}/{id_}").status_code == 401
            assert client.delete(f"{url}/{id_}").status_code == 401
