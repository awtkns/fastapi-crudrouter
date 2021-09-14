import pytest
from fastapi import APIRouter

from .implementations import implementations
from .conftest import yield_test_client


URLs = ["/potato", "/carrot"]
PARAMS = [-1, 0, 1, 14, "ten"]

GET_ALL = "Overloaded Get All"
GET_ONE = "Overloaded Get One"
CREATE_ONE = "Overloaded Post One"
UPDATE_ONE = "Overloaded Update One"
DELETE_ONE = "Overloaded Delete One"
DELETE_ALL = "Overloaded Delete All"
CUSTOM_ROUTE = "Custom Route"


@pytest.fixture(params=implementations, scope="class")
def overloaded_client(request):
    impl, dsn = request.param

    app, router, settings = impl(db_uri=dsn)
    routers = [router(**s) for s in settings]

    for r in routers:
        r: APIRouter

        @r.api_route("", methods=["GET"])
        def overloaded_get_all():
            return GET_ALL

        @r.get("/{item_id}")
        def overloaded_get_one():
            return GET_ONE

        @r.post("")
        def overloaded_get():
            return CREATE_ONE

        @r.put("/{item_id}")
        def overloaded_update():
            return UPDATE_ONE

        @r.delete("/{item_id}")
        def overloaded_delete():
            return DELETE_ONE

        @r.api_route("", methods=["DELETE"])
        def overloaded_delete():
            return DELETE_ALL

        @r.post("/custom")
        def custom_route():
            return CUSTOM_ROUTE

        app.include_router(r)

    yield from yield_test_client(app, impl)


@pytest.fixture(params=URLs)
def url(request):
    yield request.param


class TestOverloads:
    @staticmethod
    def check_response(res, expected):
        assert res.status_code == 200
        assert expected in res.text

    def test_get_all(self, overloaded_client, url):
        return self.check_response(overloaded_client.get(url), GET_ALL)

    @pytest.mark.parametrize("id_", PARAMS)
    def test_get_one(self, overloaded_client, url, id_):
        self.check_response(overloaded_client.get(f"{url}/{id_}"), GET_ONE)

    def test_create(self, overloaded_client, url):
        self.check_response(overloaded_client.post(url), CREATE_ONE)

    @pytest.mark.parametrize("id_", PARAMS)
    def test_update(self, overloaded_client, url, id_):
        self.check_response(overloaded_client.put(f"{url}/{id_}"), UPDATE_ONE)

    @pytest.mark.parametrize("id_", PARAMS)
    def test_delete(self, overloaded_client, url, id_):
        self.check_response(overloaded_client.delete(f"{url}/{id_}"), DELETE_ONE)

    def test_delete_all(self, overloaded_client, url):
        self.check_response(overloaded_client.delete(url), DELETE_ALL)

    def test_custom_route(self, overloaded_client, url):
        self.check_response(overloaded_client.post(f"{url}/custom"), CUSTOM_ROUTE)
