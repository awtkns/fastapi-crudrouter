import pytest

from . import test_router

basic_potato = dict(mass=1.2, color="Brown")

PotatoUrl = "/defaultfactorypotato"


def test_get(client):
    test_router.test_get(client, PotatoUrl)


def test_post(client):
    test_router.test_post(client, PotatoUrl, basic_potato)


def test_get_one(client):
    test_router.test_get_one(client, PotatoUrl, basic_potato)


def test_update(client):
    test_router.test_update(client, PotatoUrl, basic_potato)


def test_delete_one(client):
    test_router.test_delete_one(client, PotatoUrl, basic_potato)


def test_delete_all(client):
    test_router.test_delete_all(client, PotatoUrl, basic_potato)


@pytest.mark.parametrize(
    "id_", [-1, 0, 4, "14", "4802ee13-6f04-40ae-b6bc-be8e9eb6ba82-dxg"]
)
def test_not_found(client, id_):
    test_router.test_not_found(client, id_, PotatoUrl, basic_potato)
