from pydantic import BaseModel

from . import test_router, PotatoType

potato_type = PotatoType(name='russet', origin="Canada")
URL = '/potato_type'


def test_get(string_pk_client):
    test_router.test_get(string_pk_client, URL)


def test_post(string_pk_client):
    test_router.test_post(string_pk_client, URL, potato_type)


def test_get_one(string_pk_client):
    test_router.test_get_one(string_pk_client, URL, PotatoType(name='kenebec', origin="Ireland"), 'name')


def test_delete_one(string_pk_client):
    test_router.test_delete_one(string_pk_client, URL, PotatoType(name='golden', origin="Ireland"), 'name')


def test_delete_all(string_pk_client):
    test_router.test_delete_all(string_pk_client, URL, PotatoType(name='red', origin="Ireland"), PotatoType(name='brown', origin="Ireland"))
