import random
import pytest

from fastapi import FastAPI, testclient
from fastapi_crudrouter import MemoryCRUDRouter

from tests import Potato

URL = "/potato"


def get_client(**kwargs):
    app = FastAPI()
    app.include_router(MemoryCRUDRouter(schema=Potato, prefix=URL, **kwargs))

    return testclient.TestClient(app)


@pytest.mark.parametrize("i", list(range(1, len(MemoryCRUDRouter.get_routes()) + 1)))
def test_exclude_internal(i):
    keys = random.sample(MemoryCRUDRouter.get_routes(), k=i)
    kwargs = {r + "_route": False for r in keys}

    router = MemoryCRUDRouter(schema=Potato, prefix=URL, **kwargs)
    assert len(router.routes) == len(MemoryCRUDRouter.get_routes()) - i


def test_exclude_delete_all():
    client = get_client(delete_all_route=False)
    assert client.delete(URL).status_code == 405
    assert client.get(URL).status_code == 200


def test_exclude_all():
    routes = MemoryCRUDRouter.get_routes()
    kwargs = {r + "_route": False for r in routes}
    client = get_client(**kwargs)

    assert client.delete(URL).status_code == 404
    assert client.get(URL).status_code == 404
    assert client.post(URL).status_code == 404
    assert client.put(URL).status_code == 404

    for id_ in [-1, 1, 0, 14]:
        assert client.get(f"{URL}/{id_}").status_code == 404
        assert client.post(f"{URL}/{id_}").status_code == 404
        assert client.put(f"{URL}/{id_}").status_code == 404
        assert client.delete(f"{URL}/{id_}").status_code == 404
