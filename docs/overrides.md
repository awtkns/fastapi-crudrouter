Should you need to add custom functionality to any of your routes any of the included routers allows you to do so.

## Overriding
Routes in the CRUDRouter can be overridden by using the standard fastapi route decorators. These include:

 -  `@router.get(path: str, *args, **kwargs)`
 -  `@router.post(path: str, *args, **kwargs)`
 -  `@router.put(path: str, *args, **kwargs)`
 -  `@router.delete(path: str, *args, **kwargs)`
 -  `@router.api_route(path: str, methods: List[str] = ['GET'], *args, **kwargs)`

!!! tip
    All of CRUDRouter's are a subclass of fastapi's [APIRouter](https://fastapi.tiangolo.com/tutorial/bigger-applications/#apirouter)
    meaning that they can be customized to your heart's content.

## Full Example
Below is an example where we are overriding the route `/potato/{item_id}` while using the MemoryCRUDRouter.

```python
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi_crudrouter import MemoryCRUDRouter as CRUDRouter

class Potato(BaseModel):
    id: int
    color: str
    mass: float

app = FastAPI()
router = CRUDRouter(model=mymodel)

@router.get('/{item_id}')
def overloaded_get_all():
    return 'My overloaded route'
```

