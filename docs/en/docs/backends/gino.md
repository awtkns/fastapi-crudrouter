Asynchronous routes will be automatically generated when using the `GinoCRUDRouter`. To use it, you must pass a 
[pydantic](https://pydantic-docs.helpmanual.io/) model, your SQLAlchemy Table, and the databases database. 
This CRUDRouter is intended to be used with the python [Gino](https://python-gino.org/) library. An example
of how to use [Gino](https://python-gino.org/) with FastAPI can be found both 
[here](https://python-gino.org/docs/en/1.0/tutorials/fastapi.html) and below.

!!! warning
    To use the `GinoCRUDRouter`, Gino **and** SQLAlchemy must be first installed.

## Minimal Example
Below is a minimal example assuming that you have already imported and created 
all the required models and database connections.

```python
router = GinoCRUDRouter(
    schema=MyPydanticModel, 
    db=db,
    db_model=MyModel
)
app.include_router(router)
```
