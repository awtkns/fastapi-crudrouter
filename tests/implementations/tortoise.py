from fastapi import FastAPI
from sqlalchemy_utils import drop_database, create_database, database_exists
from tortoise import Model, fields
from tortoise.contrib.fastapi import register_tortoise
from fastapi_crudrouter import TortoiseCRUDRouter

DATABASE_URL = "sqlite://db.sqlite3"
TORTOISE_CONFIG = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": ["example"],
            "default_connection": "default",
        },
    },
}

async def _setup_base_app():
    if database_exists(DATABASE_URL):
        drop_database(DATABASE_URL)

    create_database(DATABASE_URL)
    await Tortoise.generate_schemas()

    app = FastAPI()
    register_tortoise(app, config=TORTOISE_CONFIG)

    return app


def tortoise_implementation():
    app = await _setup_base_app()

    class PotatoModel(Model):
        thickness = fields.FloatField(description="Thickness of your potato")
        mass = fields.FloatField(description="Mass of your potato")
        color = fields.CharField(max_length=255)
        type = fields.CharField(max_length=255)

    class CarrotModel(Model):
        length = fields.FloatField()
        color = fields.CharField(max_length=255)

    app.include_router(TortoiseCRUDRouter(schema=Potato, db_model=PotatoModel, db=session, prefix='potato'))
    app.include_router(TortoiseCRUDRouter(schema=Carrot, db_model=CarrotModel, db=session, create_schema=CarrotCreate, prefix='carrot'))

    return app
