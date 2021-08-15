import pytest
from fastapi import Depends, HTTPException

from tests.conftest import yield_test_client
from tests.implementations import implementations

URLS = ["/potato", "/carrot"]
AUTH = {"Authorization": "Bearer my_token"}


class RaisesException:
    def __init__(self, status_code: int):
        self.status_code = status_code

    def __call__(self):
        raise HTTPException(self.status_code)


class NullDependency:
    def __init__(self, status_code: int):
        self.status_code = status_code

    def __call__(self):
        pass


DEPENDS_KWARGS = dict(
    get_all_route=[Depends(NullDependency), Depends(RaisesException(401))],
    get_one_route=[Depends(NullDependency), Depends(RaisesException(402))],
    create_route=[Depends(NullDependency), Depends(RaisesException(403))],
    update_route=[Depends(NullDependency), Depends(RaisesException(404))],
    delete_all_route=[Depends(NullDependency), Depends(RaisesException(405))],
    delete_one_route=[Depends(NullDependency), Depends(RaisesException(406))],
)


@pytest.fixture(params=implementations)
def client(request):
    impl, dsn = request.param

    app, router, settings = impl(db_uri=dsn)
    [app.include_router(router(**s, **DEPENDS_KWARGS)) for s in settings]

    yield from yield_test_client(app, impl)


@pytest.mark.parametrize("url", URLS)
def test_route_disable(client, url):
    item_url = f"{url}/1"
    actions = [
        (client.get, url),
        (client.get, item_url),
        (client.post, url),
        (client.put, item_url),
        (client.delete, url),
        (client.delete, item_url),
    ]

    err_codes = set()
    for method, url in actions:
        print(method, url, err_codes)
        status_code = method(url).status_code

        assert status_code != 200
        assert 400 <= status_code <= 406
        assert status_code not in err_codes

        err_codes.add(status_code)

    assert len(err_codes) == len(actions)
