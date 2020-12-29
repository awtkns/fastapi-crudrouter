import pytest

from . import Potato, Carrot, test_router

basic_potato = Potato(id=0, thickness=.24, mass=1.2, color='Brown', type='Russet')
basic_carrot = Carrot(id=0, length=1.2, color='Orange')

PotatoUrl = '/potato'
CarrotUrl = '/carrot'


def test_get(custom_id_client):
    test_router.test_get(custom_id_client, PotatoUrl)


def test_post(custom_id_client):
    test_router.test_post(custom_id_client, PotatoUrl, basic_potato)


def test_get_one(custom_id_client):
    test_router.test_get_one(custom_id_client, PotatoUrl, basic_potato)


def test_update(custom_id_client):
    test_router.test_update(custom_id_client, PotatoUrl, basic_potato)


def test_delete_one(custom_id_client):
    test_router.test_delete_one(custom_id_client, PotatoUrl, basic_potato)


def test_delete_all(custom_id_client):
    test_router.test_delete_all(custom_id_client, PotatoUrl, basic_potato)


@pytest.mark.parametrize('id_', [-1, 0, 4, '14'])
def test_not_found(custom_id_client, id_):
    test_router.test_not_found(custom_id_client, id_, PotatoUrl, basic_potato)

