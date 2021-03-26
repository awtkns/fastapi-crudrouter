from fastapi import FastAPI

from fastapi_crudrouter import MemoryCRUDRouter as CRUDRouter
from tests import Potato


def overloaded_app():
    app = FastAPI()

    router = CRUDRouter(schema=Potato)

    @router.api_route("")
    def overloaded_get():
        return "Overloaded"

    @router.get("/{item_id}")
    def overloaded_get_all():
        return "Overloaded Get All"

    @router.put("/{item_id}")
    def overloaded_put():
        return "Overloaded Put"

    @router.delete("/{item_id}")
    def overloaded_delete():
        return "Overloaded DELETE"

    @router.post("")
    def overloaded_get():
        return "Overloaded Post"

    @router.api_route("", methods=["DELETE"])
    def overloaded_get():
        return "Overloaded DELETE All"

    app.include_router(router)

    return app
