import asyncio

from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

from fastapi_crudrouter import TortoiseCRUDRouter
from tests.implementations.models import PotatoModel, CarrotModel

TORTOISE_ORM = {
    "connections": {"default": 'sqlite://db.sqlite3'},
    "apps": {
        "models": {
            "models": ["tests.implementations.models"],
            "default_connection": "default",
        },
    },
}

async def setup(app):
    import os
    os.system('rm db.sqlite3 db.sqlite3-wal db.sqlite3-shm')

    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()

    Potato = pydantic_model_creator(PotatoModel, name="Potato")
    Carrot = pydantic_model_creator(CarrotModel, name="Carrot")
    CarrotCreate = pydantic_model_creator(CarrotModel, name="CarrotCreate", exclude_readonly=True)

    app.include_router(TortoiseCRUDRouter(schema=Potato, db_model=PotatoModel, prefix='potato'))
    app.include_router(
        TortoiseCRUDRouter(schema=Carrot, db_model=CarrotModel, create_schema=CarrotCreate, prefix='carrot'))

async def some_shutdown_task():
    await Tortoise.close_connections()

def tortoise_implementation():
    app = FastAPI(on_shutdown=[some_shutdown_task])
    asyncio.run(setup(app))

    return app
