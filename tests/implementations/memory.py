from fastapi import FastAPI

from fastapi_crudrouter import MemoryCRUDRouter
from tests import (
    Potato,
    DefaultFactoryPotato,
    Carrot,
    CarrotUpdate,
    PAGINATION_SIZE,
    CUSTOM_TAGS,
    POTATO_TAGS,
)


def memory_implementation(**kwargs):
    app = FastAPI()
    router_settings = [
        dict(schema=Potato, paginate=PAGINATION_SIZE),
        dict(schema=DefaultFactoryPotato, paginate=PAGINATION_SIZE, tags=POTATO_TAGS),
        dict(schema=Carrot, update_schema=CarrotUpdate, tags=CUSTOM_TAGS),
    ]

    return app, MemoryCRUDRouter, router_settings


if __name__ == "__main__":
    import uvicorn

    app, route_type, routes = memory_implementation()
    for route in routes:
        app.include_router(route_type(**route))
    uvicorn.run(app, port=5000)
