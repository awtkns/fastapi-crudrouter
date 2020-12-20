from pydantic import BaseModel
from fastapi import FastAPI

from fastapi_crudrouter import MemoryCRUDRouter as CRUDRouter

app = FastAPI(title='FastAPI-CRUDRouter', docs_url='/')


class Potato(BaseModel):
    id: int
    thickness: float
    color: str


app.include_router(CRUDRouter(model=Potato))
