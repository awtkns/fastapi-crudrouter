from fastapi import FastAPI

from fastapi_crudrouter import MemoryCRUDRouter as CRUDRouter
from tests import Potato, Carrot


def memory_implementation():
    app = FastAPI()
    app.include_router(CRUDRouter(model=Potato))
    app.include_router(CRUDRouter(model=Carrot))

    return app
