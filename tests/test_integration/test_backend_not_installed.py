import pathlib


def test_virtualenv(virtualenv):
    file = pathlib.Path(__file__)
    package = file.parent.parent.parent
    assert (package / "fastapi_crudrouter").exists()

    virtualenv.run(f"pip install -e {package}")
    virtualenv.run(f"python {file}")


if __name__ == "__main__":
    from fastapi_crudrouter import (
        SQLAlchemyCRUDRouter,
        DatabasesCRUDRouter,
        OrmarCRUDRouter,
        TortoiseCRUDRouter,
    )

    routers = [
        SQLAlchemyCRUDRouter,
        DatabasesCRUDRouter,
        OrmarCRUDRouter,
        TortoiseCRUDRouter,
    ]

    for crud_router in routers:
        try:
            # noinspection PyTypeChecker
            crud_router(..., ..., ..., ...)
        except AssertionError:
            pass
        except Exception:
            raise AssertionError(
                f"Not checking that all requirements are installed when initializing the {crud_router.__name__}"
            )
