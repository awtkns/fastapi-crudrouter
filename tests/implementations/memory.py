from fastapi_crudrouter import MemoryCRUDRouter

from tests import Potato, Carrot, CarrotUpdate, PAGINATION_SIZE, CUSTOM_TAGS
from tests.implementations import BaseImpl
from tests.implementations._base import SETTINGS


class MemoryImpl(BaseImpl):
    __router__ = MemoryCRUDRouter
    __backends__ = ["memory"]

    def default_impl(self) -> SETTINGS:
        return [
            dict(schema=Potato, paginate=PAGINATION_SIZE),
            dict(schema=Carrot, update_schema=CarrotUpdate, tags=CUSTOM_TAGS),
        ]

    def integrity_errors_impl(self) -> SETTINGS:
        pass
