from . import test_router

potato_type = dict(name="russet", origin="Canada")
URL = "/potato_type"


def test_get(string_pk_client):
    test_router.test_get(string_pk_client, URL)


def test_post(string_pk_client):
    test_router.test_post(string_pk_client, URL, potato_type)


def test_get_one(string_pk_client):
    test_router.test_get_one(
        string_pk_client, URL, dict(name="kenebec", origin="Ireland"), "name"
    )


def test_delete_one(string_pk_client):
    test_router.test_delete_one(
        string_pk_client, URL, dict(name="golden", origin="Ireland"), "name"
    )


def test_delete_all(string_pk_client):
    test_router.test_delete_all(
        string_pk_client,
        URL,
        dict(name="red", origin="Ireland"),
        dict(name="brown", origin="Ireland"),
    )
