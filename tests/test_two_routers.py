import pytest

from . import test_router
from .utils import compare_dict

basic_potato = dict(thickness=0.24, mass=1.2, color="Brown", type="Russet")
basic_carrot = dict(length=1.2, color="Orange")

PotatoUrl = "/potato"
CarrotUrl = "/carrot"


def test_get(client):
    test_router.test_get(client, PotatoUrl)
    test_router.test_get(client, CarrotUrl)


def test_post(client):
    test_router.test_post(client, PotatoUrl, basic_potato)
    test_router.test_post(client, CarrotUrl, basic_carrot)


def test_get_one(client):
    test_router.test_get_one(client, PotatoUrl, basic_potato)
    test_router.test_get_one(client, CarrotUrl, basic_carrot)


def test_update(client):
    test_router.test_update(client, PotatoUrl, basic_potato)

    with pytest.raises(AssertionError):
        test_router.test_update(client, CarrotUrl, basic_carrot)

    res = client.post(CarrotUrl, json=basic_carrot)
    data = res.json()
    assert res.status_code == 200

    carrot = {k: v for k, v in basic_carrot.items()}
    carrot["color"] = "Red"
    carrot["length"] = 54.0

    res = client.put(f'{CarrotUrl}/{data["id"]}', json=carrot)
    assert res.status_code == 200
    assert not compare_dict(res.json(), carrot, exclude=["id"])
    assert not compare_dict(res.json(), basic_carrot, exclude=["id"])
    assert compare_dict(res.json(), carrot, exclude=["id", "color"])

    res = client.get(f'{CarrotUrl}/{data["id"]}')
    assert res.status_code == 200
    assert not compare_dict(res.json(), carrot, exclude=["id"])
    assert not compare_dict(res.json(), basic_carrot, exclude=["id"])
    assert compare_dict(res.json(), carrot, exclude=["id", "color"])


def test_delete_one(client):
    test_router.test_delete_one(client, PotatoUrl, basic_potato)
    test_router.test_delete_one(client, CarrotUrl, basic_carrot)


def test_delete_all(client):
    test_router.test_delete_all(client, PotatoUrl, basic_potato)
    test_router.test_delete_all(client, CarrotUrl, basic_carrot, basic_carrot)


@pytest.mark.parametrize("id_", [-1, 0, 4, "14"])
def test_not_found(client, id_):
    test_router.test_not_found(client, id_, PotatoUrl, basic_potato)
    test_router.test_not_found(client, id_, CarrotUrl, basic_carrot)
