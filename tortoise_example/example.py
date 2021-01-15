import uvicorn as uvicorn
from fastapi import FastAPI
from flaxx.pydantic_schema_generator import pydantic_model_creator
from tortoise.contrib.fastapi import register_tortoise

from tortoise.models import Model
from tortoise import fields, Tortoise, run_async

TORTOISE_ORM = {
    "connections": {"default": 'postgres://tim:pass@localhost:5432/recipe'},
    "apps": {
        "models": {
            "models": ["example"],
            "default_connection": "default",
        },
    },
}

# Create Database Tables
async def init():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()


# Tortoise Model
class TestModel(Model):
    test = fields.IntField(null=False, description=f"Test value")
    ts = fields.IntField(null=False, description=f"Epoch time")


app = FastAPI()

register_tortoise(app, config=TORTOISE_ORM)

# Pydantic schema
TestSchema = pydantic_model_creator(TestModel, name=f"{TestModel.__name__}Schema")

from fastapi_crudrouter.core.tortoise import TortoiseCRUDRouter

router = TortoiseCRUDRouter(schema=TestSchema, db_model=TestModel, prefix="test", config=TORTOISE_ORM)

app.include_router(router)

if __name__ == "__main__":
    run_async(uvicorn.run("example:app", host="127.0.0.1", port=5000, log_level="info"))
