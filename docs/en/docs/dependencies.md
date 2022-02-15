All the CRUDRouters included with `fastapi_crudrouter` support FastAPI dependency injection.

!!! tip
    Since all CRUDRouter's subclass the [FastAPI APIRouter](https://fastapi.tiangolo.com/tutorial/bigger-applications/?h=+router#apirouter),
    you can use any features APIRouter features.

Below is a simple example of how you could use OAuth2 in conjunction with a CRUDRouter to secure your routes.

```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi_crudrouter import MemoryCRUDRouter

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def token_auth(token: str=Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(401, "Invalid token")

router = MemoryCRUDRouter(schema=MySchema, dependencies=[Depends(token_auth)])
app.include_router(router)
```

## Custom Dependencies Per Route
All CRUDRouters allow you to add a sequence of dependencies on a per-route basis. The dependencies can be set when 
initializing any CRUDRouter using the key word arguments below.

```python
CRUDRouter(
    # ...
    get_all_route=[Depends(get_all_route_dep), ...],
    get_one_route=[Depends(get_one_route_dep), ...],
    create_route=[Depends(create_route_dep), ...],
    update_route=[Depends(update_route_dep), ...],
    delete_one_route=[Depends(user), ...],
    delete_all_route=[Depends(user), ...],
)

```

!!! tip "Multiple Dependencies Per Route"
    As they are passed as a sequence, you are able to set multiple dependencies individually per route. 

!!! attention "Disabling Routes Entirely"
    Setting the key word arguments shown above to `False`, disables the route entirely.


### Example
In the example below, we are adding a fictitious dependency to the "create route" (POST) which requires the user to be 
logged in to create an object. At the same time, we are also independently adding an admin dependency to only the "delete all 
route" which limits the route's usage to only admin users.

```python
MemoryCRUDRouter(
    schema=MySchema,
    create_route=[Depends(user)],
    delete_all_route=[Depends(admin)]
)
```


