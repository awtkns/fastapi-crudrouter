import pytest

from . import Potato, Carrot, test_router
from .utils import compare_dict

PotatoUrl = '/potato'
CarrotUrl = '/carrot'

INSERT_COUNT = 20
PAGINATION_SIZE = 10


@pytest.mark.parametrize('offset', [0, 1, 5, 10, 20, 40])
@pytest.mark.parametrize('limit', [1, 10, 20])
def test_pagination(client, limit, offset):
    for i in range(INSERT_COUNT):
        test_router.test_post(client, PotatoUrl, expected_length=i+1 if i+1 < PAGINATION_SIZE else PAGINATION_SIZE)

    expected_length = limit
    if offset >= INSERT_COUNT:
        expected_length = 0

    elif offset + limit >= INSERT_COUNT:
        expected_length = INSERT_COUNT - offset

    test_router.test_get(
        client=client,
        url=PotatoUrl,
        params={'limit': limit, 'skip': offset},
        expected_length=expected_length
    )


# @pytest.mark.parametrize('offset', [-1, 'asdas', 3.23])
# def test_invalid_offset(client, offset):
#     for i in range(INSERT_COUNT):
#         test_router.test_post(client, PotatoUrl, expected_length=i+1 if i+1 < PAGINATION_SIZE else PAGINATION_SIZE)
#
#     test_router.test_get(
#         client=client,
#         url=PotatoUrl,
#         params={'skip': offset},
#         expected_length=expected_length
#     )



