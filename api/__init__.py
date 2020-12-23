from pydantic import BaseModel
from fastapi import FastAPI
from starlette.routing import Route

from fastapi_crudrouter import MemoryCRUDRouter as CRUDRouter

app = FastAPI(title='FastAPI-CRUDRouter', docs_url='/')


class Potato(BaseModel):
    id: int
    thickness: float
    color: str

router = CRUDRouter(model=Potato)


@router.api_route('')
def custom_getds():
    return 'ok'

@router.put('')
def my_put():
    return 'ok'


for r in router.routes:
    print(r.path)



app.include_router(router)
