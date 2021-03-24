import typing

import pytest

from . import PAGINATION_SIZE, test_router

PotatoUrl = "/potato"
CarrotUrl = "/carrot"
basic_carrot = dict(length=1.2, color="Orange")
basic_potato = dict(thickness=0.24, mass=1.2, color="Brown", type="Russet")

INSERT_COUNT = 20


@pytest.fixture(scope="class")
def insert_items(
    client,
    url: str = PotatoUrl,
    model: typing.Dict = None,
    count: int = INSERT_COUNT,
):
    model = model or basic_potato
    for i in range(count):
        test_router.test_post(
            client,
            url=url,
            model=model,
            expected_length=i + 1 if i + 1 < PAGINATION_SIZE else PAGINATION_SIZE,
        )


@pytest.fixture(scope="class")
def insert_carrots(client):
    for i in range(INSERT_COUNT):
        test_router.test_post(client, CarrotUrl, basic_carrot, expected_length=i + 1)


@pytest.fixture(scope="class")
def cleanup(client):
    yield
    client.delete(CarrotUrl)
    client.delete(PotatoUrl)


def get_expected_length(limit, offset, count: int = INSERT_COUNT):
    expected_length = limit
    if offset >= count:
        expected_length = 0

    elif offset + limit >= INSERT_COUNT:
        expected_length = INSERT_COUNT - offset

    return expected_length


@pytest.mark.usefixtures("insert_carrots", "insert_items", "cleanup")
class TestPagination:
    @pytest.mark.parametrize("offset", [0, 1, 5, 10, 20, 40])
    @pytest.mark.parametrize("limit", [1, 5, 10])
    def test_pagination(self, client, limit, offset):
        test_router.test_get(
            client=client,
            url=PotatoUrl,
            params={"limit": limit, "skip": offset},
            expected_length=get_expected_length(limit, offset),
        )

    @pytest.mark.parametrize("offset", [-1, "asdas", 3.23])
    def test_invalid_offset(self, client, offset):
        res = client.get(PotatoUrl, params={"skip": offset})
        assert res.status_code == 422

    @pytest.mark.parametrize("limit", [-1, 0, "asdas", 3.23, 21])
    def test_invalid_limit(self, client, limit):
        res = client.get(PotatoUrl, params={"limit": limit})
        assert res.status_code == 422

    def test_pagination_disabled(self, client):
        test_router.test_get(client, CarrotUrl, expected_length=INSERT_COUNT)

    @pytest.mark.parametrize("limit", [2, 5, 10])
    def test_paging(self, client, limit):
        ids = set()
        skip = 0
        while skip < INSERT_COUNT:
            data = test_router.test_get(
                client,
                PotatoUrl,
                params={"limit": limit, "skip": skip},
                expected_length=get_expected_length(limit, skip),
            )

            for item in data:
                assert item["id"] not in ids
                ids.add(item["id"])

            skip += limit

        assert len(ids) == INSERT_COUNT

    @pytest.mark.parametrize("limit", [2, 5, 10])
    def test_paging_no_limit(self, client, limit):
        client.delete(CarrotUrl)
        for i in range(limit):
            res = client.post(url=CarrotUrl, json=basic_carrot)
            assert res.status_code == 200, res.json()

        res = client.get(CarrotUrl)
        assert res.status_code == 200, res.json()
        assert len(res.json()) == limit

        res = client.get(CarrotUrl, params={"limit": limit})
        assert res.status_code == 200, res.json()
        assert len(res.json()) == limit

        limit = int(limit / 2)
        res = client.get(CarrotUrl, params={"limit": limit})
        assert res.status_code == 200, res.json()
        assert len(res.json()) == limit
