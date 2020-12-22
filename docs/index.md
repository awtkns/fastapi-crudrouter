<p align="center">
  <img src="assets/logo2.png" alt="CRUD Router Logo" height="200" />
</p>
<p align="center">
  <em>⚡ Create CRUD routes with lighting speed</em> ⚡</br>
  <sub>A dynamic FastAPI router that automatically creates routes CRUD for your models</sub>
</p>
<p align="center">
<img alt="Tests" src="https://github.com/awtkns/fastapi-crudrouter/workflows/Python%20application/badge.svg" />
<img alt="Docs" src="https://github.com/awtkns/fastapi-crudrouter/workflows/docs/badge.svg" />
<img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/fastapi" />
</p>

---
## Installation

<div id="termynal" data-termynal>
    <span data-ty="input">pip install fastapi-crudrouter</span>
    <span data-ty="progress"></span>
    <span data-ty>Successfully installed fastapi-crudrouter</span>
</div>


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