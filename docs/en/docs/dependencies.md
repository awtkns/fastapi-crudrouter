All the CRUDRouters included with `fastapi_crudrouter` support FastAPI dependency injection.

!!! tip
    Since all CRUDRouter's subclass the [FastAPI APIRouter](https://fastapi.tiangolo.com/tutorial/bigger-applications/?h=+router#apirouter),
    you can use any features APIRouter features.

## Example
Below is a simple example of how you could use OAuth2 in conjunction with a CRUDRouter to secure your routes.

```python
from fastapi import FastAPI, testclient, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi_crudrouter import MemoryCRUDRouter

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def token_auth(token: str):
    if not token:
        raise HTTPException(401, "Invalid token")

router = MemoryCRUDRouter(schema=Potato, dependencies=[Depends(token_auth)])
app.include_router(router)
```