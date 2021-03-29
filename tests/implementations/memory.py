from fastapi import FastAPI

from fastapi_crudrouter import MemoryCRUDRouter as CRUDRouter
from tests import Potato, Carrot, CarrotUpdate, PAGINATION_SIZE


def memory_implementation():
    app = FastAPI()
    potato_router = CRUDRouter(schema=Potato, paginate=PAGINATION_SIZE)
    carrot_router = CRUDRouter(schema=Carrot, update_schema=CarrotUpdate)

    return app, [potato_router, carrot_router]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(memory_implementation(), port=5000)
