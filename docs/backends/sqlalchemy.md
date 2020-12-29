```python
from sqlalchemy import Column, String, Float, Integer
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from pydantic import BaseModel
from fastapi import FastAPI
from fastapi_crudrouter import SQLAlchemyCRUDRouter

app = FastAPI()
engine = create_engine("sqlite:///./app.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    finally:
        session.close()

class PotatoCreate(BaseModel):
    thickness: float
    mass: float
    color: str
    type: str


class Potato(PotatoCreate):
    id: int

    class Config:
        orm_mode = True

class PotatoModel(Base):
    __tablename__ = 'potatoes'
    id = Column(Integer, primary_key=True, index=True)
    thickness = Column(Float)
    mass = Column(Float)
    color = Column(String)
    type = Column(String)

Base.metadata.create_all(bind=engine)
app.include_router(SQLAlchemyCRUDRouter(model=Potato, db_model=PotatoModel, db=session, create_schema=PotatoCreate, prefix='potato'))

```