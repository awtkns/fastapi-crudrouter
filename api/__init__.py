from pydantic import BaseModel
from fastapi import FastAPI
from starlette.routing import Route

from fastapi_crudrouter import MemoryCRUDRouter as CRUDRouter

app = FastAPI(title='FastAPI-CRUDRouter', docs_url='/')


class Potato(BaseModel):
    id: int
    thickness: float
    color: str

class CarrotModel(Base):
    __tablename__ = 'carrots'
    id = Column(Integer, primary_key=True, index=True)
    length = Column(Float)
    color = Column(String)

