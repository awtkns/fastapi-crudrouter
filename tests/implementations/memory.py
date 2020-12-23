from fastapi import FastAPI

from fastapi_crudrouter import MemoryCRUDRouter as CRUDRouter
from tests import Potato


def memory_implementation():
    app = FastAPI()
    app.include_router(CRUDRouter(model=Potato))

    return app
