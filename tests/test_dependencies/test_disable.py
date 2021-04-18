from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

import pytest

from fastapi_crudrouter.core import CRUDGenerator

from tests.implementations import implementations
from tests.conftest import yield_test_client

URLS = ["/potato", "/carrot"]
AUTH = {"Authorization": "Bearer my_token"}
KEY_WORDS = {f"{r}_route" for r in CRUDGenerator.get_routes()}
DISABLE_KWARGS = {k: False for k in KEY_WORDS}


@pytest.fixture(params=implementations, scope="class")
def client(request):
    impl = request.param

    app, router, settings = impl()
    [app.include_router(router(**s, **DISABLE_KWARGS)) for s in settings]

    yield from yield_test_client(app, impl)


@pytest.mark.parametrize("url", URLS)
def test_route_disable(client, url):
    assert client.get(url).status_code == 404
    assert client.get(url).status_code == 404
    assert client.post(url).status_code == 404

    for id_ in [-1, 1, 0, 14]:
        assert client.get(f"{url}/{id_}").status_code == 404
        assert client.put(f"{url}/{id_}").status_code == 404
        assert client.delete(f"{url}/{id_}").status_code == 404
