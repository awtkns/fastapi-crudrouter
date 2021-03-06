from fastapi import FastAPI

from fastapi_crudrouter import MemoryCRUDRouter as CRUDRouter
from tests import Potato, Carrot, CarrotUpdate, PAGINATION_SIZE


def memory_implementation():
    app = FastAPI()
    app.include_router(CRUDRouter(schema=Potato, paginate=PAGINATION_SIZE))
    app.include_router(CRUDRouter(schema=Carrot, update_schema=CarrotUpdate))

    return app
