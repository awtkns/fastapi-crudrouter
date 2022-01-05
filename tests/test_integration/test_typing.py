import pathlib

file = pathlib.Path(__file__)
package = file.parent.parent.parent / "fastapi_crudrouter"


def test_py_typed_file_exists():
    assert (package / "py.typed").exists()
    assert (package / "py.typed").is_file()


def test_virtualenv(virtualenv):
    assert (package).exists()

    virtualenv.run(f"pip install -e {package}")
    virtualenv.run(f"pip install mypy")
    virtualenv.run(f"mypy {file}")


if __name__ == "__main__":
    from pydantic import BaseModel
    from fastapi import FastAPI

    import fastapi_crudrouter

    class User(BaseModel):
        id: int
        name: str
        email: str

    router = fastapi_crudrouter.MemoryCRUDRouter(schema=User)
    app = FastAPI()
    app.include_router(router)
