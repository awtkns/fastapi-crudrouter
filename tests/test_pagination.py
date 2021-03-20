import typing
import pytest


from . import Potato, Carrot, test_router, PAGINATION_SIZE
from .utils import compare_dict

PotatoUrl = '/potato'
CarrotUrl = '/carrot'
basic_carrot = Carrot(id=0, length=1.2, color='Orange')
basic_potato = Potato(id=0, thickness=.24, mass=1.2, color='Brown', type='Russet')

INSERT_COUNT = 20


def insert_items(client, url: str = PotatoUrl, model: typing.Union[Carrot, Potato] = basic_potato, count: int = INSERT_COUNT):
    for i in range(count):
        test_router.test_post(
            client,
            url=url,
            model=model,
            expected_length=i + 1 if i + 1 < PAGINATION_SIZE else PAGINATION_SIZE
        )


def get_expected_length(limit, offset, count: int = INSERT_COUNT):
    expected_length = limit
    if offset >= count:
        expected_length = 0

    elif offset + limit >= INSERT_COUNT:
        expected_length = INSERT_COUNT - offset

    return expected_length


@pytest.mark.parametrize('offset', [0, 1, 5, 10, 20, 40])
@pytest.mark.parametrize('limit', [1, 5, 10])
def test_pagination(client, limit, offset):
    insert_items(client)
    test_router.test_get(
        client=client,
        url=PotatoUrl,
        params={'limit': limit, 'skip': offset},
        expected_length=get_expected_length(limit, offset)
    )


@pytest.mark.parametrize('offset', [-1, 'asdas', 3.23])
def test_invalid_offset(client, offset):
    insert_items(client)
    res = client.get(PotatoUrl, params={'skip': offset})
    assert res.status_code == 422


@pytest.mark.parametrize('limit', [-1, 0, 'asdas', 3.23, 21])
def test_invalid_limit(client, limit):
    insert_items(client)
    res = client.get(PotatoUrl, params={'limit': limit})
    assert res.status_code == 422


def test_pagination_disabled(client):
    for i in range(INSERT_COUNT):
        test_router.test_post(client, CarrotUrl, basic_carrot, expected_length=i + 1)

    test_router.test_get(client, CarrotUrl, expected_length=INSERT_COUNT)


@pytest.mark.parametrize('limit', [2, 5, 10])
def test_paging(client, limit):
    insert_items(client)

    ids = set()
    skip = 0
    while skip < INSERT_COUNT:
        data = test_router.test_get(
            client,
            PotatoUrl,
            params={'limit': limit, 'skip': skip},
            expected_length=get_expected_length(limit, skip)
        )

        for item in data:
            assert item['id'] not in ids
            ids.add(item['id'])

        skip += limit

    assert len(ids) == INSERT_COUNT


@pytest.mark.parametrize('limit', [2, 5, 10])
def test_paging_no_limit(client, limit):
    for i in range(limit):
        res = client.post(url=CarrotUrl, json=basic_carrot.dict())
        assert res.status_code == 200, res.json()

    res = client.get(CarrotUrl)
    assert res.status_code == 200, res.json()
    assert len(res.json()) == limit

    res = client.get(CarrotUrl, params={'limit': limit})
    assert res.status_code == 200, res.json()
    assert len(res.json()) == limit

    limit = int(limit / 2)
    res = client.get(CarrotUrl, params={'limit': limit})
    assert res.status_code == 200, res.json()
    assert len(res.json()) == limit

