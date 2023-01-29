Asynchronous routes will be automatically generated when using the `DatabasesCRUDRouter`. To use it, you must pass a 
[pydantic](https://pydantic-docs.helpmanual.io/) model, your SQLAlchemy Table, and the databases database. 
This CRUDRouter is intended to be used with the python [Databases](https://www.encode.io/databases/) library. An example
of how to use [Databases](https://www.encode.io/databases/) with FastAPI can be found both 
[here](https://fastapi.tiangolo.com/advanced/async-sql-databases/) and below.

!!! warning
    To use the `DatabasesCRUDRouter`, Databases **and** SQLAlchemy must be first installed.

## Minimal Example
Below is a minimal example assuming that you have already imported and created 
all the required models and database connections.

```python
from fastapi_crudrouter import DatabasesCRUDRouter
from fastapi import FastAPI

app = FastAPI()

router = DatabasesCRUDRouter(
    schema=MyPydanticModel, 
    table=my_table,
    database=my_database
)
app.include_router(router)
```

## Full Example

```python
import databases
import sqlalchemy

from pydantic import BaseModel
from fastapi import FastAPI
from fastapi_crudrouter import DatabasesCRUDRouter

DATABASE_URL = "sqlite:///./test.db"

database = databases.Database(DATABASE_URL)
engine = sqlalchemy.create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

metadata = sqlalchemy.MetaData()
potatoes = sqlalchemy.Table(
    "potatoes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("thickness", sqlalchemy.Float),
    sqlalchemy.Column("mass", sqlalchemy.Float),
    sqlalchemy.Column("color", sqlalchemy.String),
    sqlalchemy.Column("type", sqlalchemy.String),
)
metadata.create_all(bind=engine)


class PotatoCreate(BaseModel):
    thickness: float
    mass: float
    color: str
    type: str


class Potato(PotatoCreate):
    id: int


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


router = DatabasesCRUDRouter(
    schema=Potato,
    create_schema=PotatoCreate,
    table=potatoes,
    database=database
)
app.include_router(router)
```