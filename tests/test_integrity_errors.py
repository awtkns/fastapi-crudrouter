import pytest

from tests import test_router

POTATO_URL = "/potatoes"


def test_integrity_error_create(integrity_errors_client):
    client = integrity_errors_client
    potato = dict(id=1, thickness=2, mass=5, color="red", type="russet")

    args = client, POTATO_URL, potato
    test_router.test_post(*args)
    with pytest.raises(AssertionError):
        test_router.test_post(*args)

    # No integrity error here because of the create_schema
    args = client, "/carrots", dict(id=1, length=2, color="red")
    test_router.test_post(*args)
    test_router.test_post(*args, expected_length=2)


def test_integrity_error_update(integrity_errors_client):
    client = integrity_errors_client
    potato1 = dict(id=1, thickness=2, mass=5, color="red", type="russet")

    potato2 = dict(id=2, thickness=9, mass=5, color="yellow", type="mini")

    args = client, POTATO_URL
    test_router.test_post(*args, potato1, expected_length=1)
    test_router.test_post(*args, potato2, expected_length=2)

    potato2["color"] = potato1["color"]
    res = client.put(f'{POTATO_URL}/{potato2["id"]}', json=potato2)
    assert res.status_code == 422, res.json()

    potato2["color"] = "green"
    res = client.put(f'{POTATO_URL}/{potato2["id"]}', json=potato2)
    assert res.status_code == 200, res.json()
