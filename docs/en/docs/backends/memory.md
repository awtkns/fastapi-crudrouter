The `MemoryCRUDRouter` is the simplest usage of the CRUDRouters.  To use it, simply pass a 
[pydantic](https://pydantic-docs.helpmanual.io/) model to it.  As a database is not required, the `MemoryCRUDRouter` is
well suited for rapid bootstrapping and prototyping.

## Usage
```python
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi_crudrouter import MemoryCRUDRouter

class Potato(BaseModel):
    id: int
    color: str
    mass: float

app = FastAPI()
router = MemoryCRUDRouter(schema=Potato)
app.include_router(router)
```

!!! warning
    When using the `MemoryCRUDRouter`, the schema (model) passed to it must have the `id: int` property.

!!! danger
    The storage for the `MemoryCRUDRouter` resides in memory, not a database. Hence, the data is not persistent. Be careful when using it beyond
    the rapid bootstrapping or prototyping phase.