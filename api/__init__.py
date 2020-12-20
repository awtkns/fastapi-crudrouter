import pydantic
from fastapi import FastAPI

from .gen import CRUDGenerator
from fastapi_crudrouter import MemoryCRUDRouter

app = FastAPI(title='FastAPI-CRUDRouter', docs_url='/')


class Item(pydantic.BaseModel):
    id: int
    name: str


class Carrot(pydantic.BaseModel):
    id: int
    thickness: float
    color: str


item_router = CRUDGenerator(model=Item)
carrot_router = MemoryCRUDRouter(model=Carrot)
app.include_router(item_router)
app.include_router(carrot_router)
