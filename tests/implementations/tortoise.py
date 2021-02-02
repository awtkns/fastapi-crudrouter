import os

from fastapi import FastAPI
from tortoise import Tortoise, Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator

from fastapi_crudrouter import TortoiseCRUDRouter


class PotatoModel(Model):
    thickness = fields.FloatField()
    mass = fields.FloatField()
    color = fields.CharField(max_length=255)
    type = fields.CharField(max_length=255)


class CarrotModel(Model):
    length = fields.FloatField()
    color = fields.CharField(max_length=255)


Potato = pydantic_model_creator(PotatoModel, name="Potato")
Carrot = pydantic_model_creator(CarrotModel, name="Carrot")
CarrotCreate = pydantic_model_creator(CarrotModel, name="CarrotCreate", exclude_readonly=True)


TORTOISE_ORM = {
    "connections": {"default": 'sqlite://db.sqlite3'},
    "apps": {
        "models": {
            "models": ["tests.implementations.tortoise"],
            "default_connection": "default",
        },
    },
}


async def on_shutdown():
    await Tortoise.close_connections()


def tortoise_implementation():
    [os.remove(f'./db.sqlite3{s}') for s in ['', '-wal', '-shm'] if os.path.exists(f'./db.sqlite3{s}')]

    app = FastAPI(on_shutdown=[on_shutdown])

    Tortoise.init(config=TORTOISE_ORM)
    Tortoise.generate_schemas()

    app.include_router(TortoiseCRUDRouter(schema=Potato, db_model=PotatoModel, prefix='potato'))
    app.include_router(TortoiseCRUDRouter(schema=Carrot, db_model=CarrotModel, create_schema=CarrotCreate, prefix='carrot'))

    return app
