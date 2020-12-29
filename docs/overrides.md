```python
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi_crudrouter import MemoryCRUDRouter as CRUDRouter

class Potato(BaseModel):
    id: int
    color: str
    mass: float

app = FastAPI()
router = CRUDRouter(model=Potato)

@router.get('/{item_id}')
def overloaded_get_all():
    return 'My overloaded route'
```