from fastapi import FastAPI
from sqlalchemy_utils import drop_database, create_database, database_exists
from tortoise import Model, fields
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

from fastapi_crudrouter import TortoiseCRUDRouter

DATABASE_URL = "sqlite:///./test.db"


def _setup_base_app():
    if database_exists(DATABASE_URL):
        drop_database(DATABASE_URL)

    create_database(DATABASE_URL)

    app = FastAPI()

    return app


def tortoise_implementation():
    app = _setup_base_app()

    class PotatoModel(Model):
        thickness = fields.FloatField(description="Thickness of your potato")
        mass = fields.FloatField(description="Mass of your potato")
        color = fields.CharField(max_length=255)
        type = fields.CharField(max_length=255)

    class CarrotModel(Model):
        length = fields.FloatField()
        color = fields.CharField(max_length=255)

    Potato = pydantic_model_creator(PotatoModel, name="Potato")
    Carrot = pydantic_model_creator(CarrotModel, name="Carrot")
    CarrotCreate = pydantic_model_creator(CarrotModel, name="CarrotCreate", exclude_readonly=True)

    app.include_router(TortoiseCRUDRouter(schema=Potato, db_model=PotatoModel, prefix='potato'))
    app.include_router(TortoiseCRUDRouter(schema=Carrot, db_model=CarrotModel, create_schema=CarrotCreate, prefix='carrot'))

    register_tortoise(
        app,
        db_url=DATABASE_URL,
        generate_schemas=True,
        add_exception_handlers=True,
    )

    return app
