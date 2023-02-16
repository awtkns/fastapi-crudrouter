from typing import Dict

import pytest

from .utils import compare_dict

basic_potato = dict(thickness=0.24, mass=1.2, color="Brown", type="Russet")
URL = "/potato"


def test_get(client, url: str = URL, params: dict = None, expected_length: int = 0):
    res = client.get(url, params=params)
    data = res.json()

    assert res.status_code == 200, data
    assert type(data) == list and len(data) == expected_length

    return data


def test_post(
    client, url: str = URL, model: Dict = None, expected_length: int = 1
) -> dict:
    model = model or basic_potato
    res = client.post(url, json=model)
    assert res.status_code == 200, res.json()

    data = client.get(url).json()
    assert len(data) == expected_length

    return res.json()


def test_get_one(client, url: str = URL, model: Dict = None, id_key: str = "id"):
    model = model or basic_potato
    res = client.post(url, json=model)
    assert res.status_code == 200
    id_ = res.json()[id_key]

    data = client.get(url).json()
    assert len(data)

    res = client.get(f"{url}/{id_}")
    assert res.status_code == 200

    assert compare_dict(res.json(), model, exclude=[id_key])


def test_update(client, url: str = URL, model: Dict = None, id_key: str = "id"):
    test_get(client, url, expected_length=0)

    model = model or basic_potato
    res = client.post(url, json=model)
    data = res.json()
    assert res.status_code == 200

    test_get(client, url, expected_length=1)

    tuber = {k: v for k, v in model.items()}
    tuber["color"] = "yellow"

    res = client.put(f"{url}/{data[id_key]}", json=tuber)
    assert res.status_code == 200
    assert compare_dict(res.json(), tuber, exclude=[id_key])
    assert not compare_dict(res.json(), model, exclude=[id_key])

    res = client.get(f"{url}/{data[id_key]}")
    assert res.status_code == 200
    assert compare_dict(res.json(), tuber, exclude=[id_key])
    assert not compare_dict(res.json(), model, exclude=[id_key])


def test_patch(client, url: str = URL, model: Dict = None, id_key: str = "id"):
    test_get(client, url, expected_length=0)

    model = model or basic_potato
    res = client.post(url, json=model)
    data = res.json()
    assert res.status_code == 200

    test_get(client, url, expected_length=1)

    tuber = {}
    tuber["color"] = "yellow"
    resp_tuber = {k: v for k, v in model.items()}
    resp_tuber["color"] = "yellow"
    res = client.patch(f"{url}/{data[id_key]}", json=tuber)
    assert res.status_code == 200
    assert compare_dict(res.json(), resp_tuber, exclude=[id_key])
    assert not compare_dict(res.json(), model, exclude=[id_key])

    res = client.get(f"{url}/{data[id_key]}")
    assert res.status_code == 200
    assert compare_dict(res.json(), resp_tuber, exclude=[id_key])
    assert not compare_dict(res.json(), model, exclude=[id_key])


def test_delete_one(client, url: str = URL, model: Dict = None, id_key: str = "id"):
    model = model or basic_potato
    res = client.post(url, json=model)
    data = res.json()
    assert res.status_code == 200

    res = client.get(f"{url}/{data[id_key]}")
    assert res.status_code == 200
    assert compare_dict(res.json(), model, exclude=[id_key])

    length_before = len(client.get(url).json())

    res = client.delete(f"{url}/{data[id_key]}")
    assert res.status_code == 200
    assert compare_dict(res.json(), model, exclude=[id_key])

    res = client.get(url)
    assert res.status_code == 200
    assert len(res.json()) < length_before


def test_delete_all(
    client,
    url: str = URL,
    model: Dict = None,
    model2: Dict = None,
):
    model = model or basic_potato
    model2 = model2 or basic_potato

    res = client.post(url, json=model)
    assert res.status_code == 200

    res = client.post(url, json=model2)
    assert res.status_code == 200

    assert len(client.get(url).json()) >= 2

    res = client.delete(url)
    assert res.status_code == 200
    assert len(res.json()) == 0

    assert len(client.get(url).json()) == 0


@pytest.mark.parametrize("id_", [-1, 0, 4, "14"])
def test_not_found(client, id_, url: str = URL, model: Dict = None):
    url = f"{url}/{id_}"
    model = model or basic_potato
    assert client.get(url).status_code == 404
    assert client.put(url, json=model).status_code == 404
    assert client.delete(url).status_code == 404


def test_dne(client):
    res = client.get("/")
    assert res.status_code == 404

    res = client.get(f"/tomatoes")
    assert res.status_code == 404
