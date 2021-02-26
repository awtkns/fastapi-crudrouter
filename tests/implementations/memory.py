from fastapi import FastAPI

from fastapi_crudrouter import MemoryCRUDRouter as CRUDRouter
from tests import Potato, Carrot, CarrotUpdate


def memory_implementation():
    app = FastAPI()
    app.include_router(CRUDRouter(schema=Potato))
    app.include_router(CRUDRouter(schema=Carrot, update_schema=CarrotUpdate))

    return app

import uvicorn

if __name__ == '__main__':
    uvicorn.run(memory_implementation())