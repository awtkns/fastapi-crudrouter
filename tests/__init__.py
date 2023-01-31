from uuid import uuid4
from pydantic import BaseModel, Field

from .conf import config

PAGINATION_SIZE = 10
CUSTOM_TAGS = ["Tag1", "Tag2"]
POTATO_TAGS = ["Potato"]


class ORMModel(BaseModel):
    id: int

    class Config:
        orm_mode = True


class PotatoCreate(BaseModel):
    thickness: float
    mass: float
    color: str
    type: str


class Potato(PotatoCreate, ORMModel):
    pass


class DefaultFactoryPotatoCreate(BaseModel):
    color: str
    mass: float


class DefaultFactoryPotato(DefaultFactoryPotatoCreate, ORMModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    pass


class CustomPotato(PotatoCreate):
    potato_id: int

    class Config:
        orm_mode = True


class CarrotCreate(BaseModel):
    length: float
    color: str = "Orange"


class CarrotUpdate(BaseModel):
    length: float


class Carrot(CarrotCreate, ORMModel):
    pass


class PotatoType(BaseModel):
    name: str
    origin: str

    class Config:
        orm_mode = True
