<p align="center">
  <img src="https://raw.githubusercontent.com/awtkns/fastapi-crudrouter/master/docs/assets/logo2.png" height="200" />
</p>
<p align="center">
  <em>⚡ Create CRUD routes with lighting speed</em> ⚡</br>
  <sub>A dynamic FastAPI router that automatically creates CRUD routes for your models</sub>
</p>
<p align="center">
<img alt="Tests" src="https://github.com/awtkns/fastapi-crudrouter/workflows/Python%20application/badge.svg" />
<img alt="Docs" src="https://github.com/awtkns/fastapi-crudrouter/workflows/docs/badge.svg" />
  <a href="https://pypi.org/project/fastapi-crudrouter" target="_blank">
    <img src="https://img.shields.io/pypi/v/fastapi-crudrouter?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
</p>

---
Tired of rewriting the same generic CRUD routes? Need to rapidly prototype a feature for a presentation
or a hackathon? Thankfully, [fastapi-crudrouter](https://github.com/awtkns/fastapi-crudrouter) has your back. As an 
extension to the APIRouter included with [FastAPI](https://fastapi.tiangolo.com/), the FastAPI CRUDRouter will automatically
generate and document your CRUD routes for you, all you have to do is pass your model and maybe your database connection.

FastAPI-CRUDRouter is also **lighting fast**, well tested, and **production ready**.


## Installation
```bash
pip install fastapi-crudrouter
```

## Usage
```python
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi_crudrouter import MemoryCRUDRouter as CRUDRouter

class Potato(BaseModel):
    id: int
    color: str
    mass: float

app = FastAPI()
app.include_router(CRUDRouter(model=Potato))

```

## Database Support

- All databases supported by SQLAlchemy

