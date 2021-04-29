from operator import itemgetter

from tests.test_router import test_post, test_get


def insert(_client):
    test_post(_client)
    test_post(_client, expected_length=2)
    test_post(_client, expected_length=3)

    test_post(
        _client,
        model=dict(thickness=0.24, mass=1.1, color="red", type="Large"),
        expected_length=4,
    )
    test_post(
        _client,
        model=dict(thickness=0.10, mass=1.9, color="red", type="Small"),
        expected_length=5,
    )
    test_post(
        _client,
        model=dict(thickness=0.25, mass=1.9, color="red", type="Medium"),
        expected_length=6,
    )


def test_simple(client):
    insert(client)

    test_get(client, params={"color": "red"}, expected_length=3)
    test_get(client, params={"color": "blue"}, expected_length=0)
    test_get(client, params={"type": "Large"}, expected_length=1)
    test_get(client, params={"thickness": 0.24}, expected_length=4)


def test_two_params(client):
    insert(client)

    test_get(client, params={"color": "red", "type": "Large"}, expected_length=1)
    test_get(client, params={"color": "red", "type": "Small"}, expected_length=1)
    test_get(client, params={"color": "blue", "type": "Small"}, expected_length=0)
    test_get(client, params={"thickness": 0.24, "mass": 1.2}, expected_length=3)


def test_sort_asc(client):
    insert(client)

    data1 = test_get(client, params={"color": "red", "sort": "thickness"}, expected_length=3)
    assert data1 == sorted(data1, key=itemgetter("thickness"))


def test_sort_desc(client):
    insert(client)

    data = test_get(client, params={"color": "red", "sort": "thickness", "direction": "desc"}, expected_length=3)
    assert data == sorted(data, key=itemgetter("thickness"), reverse=True)


