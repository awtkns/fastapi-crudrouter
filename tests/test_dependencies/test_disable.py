import pytest

from fastapi_crudrouter.core import CRUDGenerator

from tests import test_router
from tests.implementations import implementations, BaseImpl
from tests.conftest import yield_test_client, label_func

URLS = ["/potato", "/carrot"]
AUTH = {"Authorization": "Bearer my_token"}
KEY_WORDS = {f"{r}_route" for r in CRUDGenerator.get_routes()}
DISABLE_KWARGS = {k: False for k in KEY_WORDS}


@pytest.fixture(params=implementations, ids=label_func, scope="class")
def client(request):
    impl: BaseImpl = request.param
    app = impl.create(**DISABLE_KWARGS)

    yield from yield_test_client(app, impl)


@pytest.fixture(params=implementations, ids=label_func, scope="class")
def delete_all_client(request):
    impl: BaseImpl = request.param
    app = impl.create(delete_all_route=False, update_route=False)

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


def test_route_disable_single(delete_all_client):
    url = "/potato"

    assert delete_all_client.delete(url).status_code == 405

    test_router.test_post(delete_all_client, url)
    assert delete_all_client.put(f"{url}/{1}").status_code == 405
    assert delete_all_client.delete(f"{url}/{1}").status_code == 200
