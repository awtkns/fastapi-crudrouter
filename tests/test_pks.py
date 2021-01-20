from pydantic import BaseModel

from . import test_router, PotatoType
from .utils import compare_dict

potato_type = PotatoType(name='russet', origin="Canada")
URL = '/potato_type'


def test_string_pks(string_pk_client):
    client = string_pk_client

    test_router.test_get(client, URL)
    test_router.test_post(client, URL, potato_type)
    test_router.test_get_one(client, URL,  PotatoType(name='kenebec', origin="Ireland"), 'name')
    test_router.test_delete_one(client, URL, PotatoType(name='golden', origin="Ireland"), 'name')
    test_router.test_delete_all(client, URL, PotatoType(name='red', origin="Ireland"), PotatoType(name='brown', origin="Ireland"))



