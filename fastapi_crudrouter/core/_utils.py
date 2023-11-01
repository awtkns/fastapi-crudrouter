from typing import Optional, Type, Any

from fastapi import Depends, HTTPException
from pydantic import create_model
from pydantic import __version__ as pydantic_version

from ._types import T, PAGINATION, PYDANTIC_SCHEMA

PYDANTIC_MAJOR_VERSION = int(pydantic_version.split(".", maxsplit=1)[0])

class AttrDict(dict):  # type: ignore
    def __init__(self, *args, **kwargs) -> None:  # type: ignore
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def get_pk_type(schema: Type[PYDANTIC_SCHEMA], pk_field: str) -> Any:
    try:
        if PYDANTIC_MAJOR_VERSION >= 2:
            return schema.model_fields[pk_field].annotation
        else:
            return schema.__fields__[pk_field].type_
    except KeyError:
        return int


def schema_factory(
    schema_cls: Type[T], pk_field_name: str = "id", name: str = "Create"
) -> Type[T]:
    """
    Is used to create a CreateSchema which does not contain pk
    """

    if PYDANTIC_MAJOR_VERSION >= 2:
        # pydantic 2.x
        fields = {
            fk: (fv.annotation, ...)
            for fk, fv in schema_cls.model_fields.items()
            if fk != pk_field_name
        }
    else:
        # pydantic 1.x
        fields = {
            f.name: (f.type_, ...)
            for f in schema_cls.__fields__.values()
            if f.name != pk_field_name
        }

    name = schema_cls.__name__ + name
    schema: Type[T] = create_model(__model_name=name, **fields)  # type: ignore
    return schema


def create_query_validation_exception(field: str, msg: str) -> HTTPException:
    return HTTPException(
        422,
        detail={
            "detail": [
                {"loc": ["query", field], "msg": msg, "type": "type_error.integer"}
            ]
        },
    )


def pagination_factory(max_limit: Optional[int] = None) -> Any:
    """
    Created the pagination dependency to be used in the router
    """

    def pagination(skip: int = 0, limit: Optional[int] = max_limit) -> PAGINATION:
        if skip < 0:
            raise create_query_validation_exception(
                field="skip",
                msg="skip query parameter must be greater or equal to zero",
            )

        if limit is not None:
            if limit <= 0:
                raise create_query_validation_exception(
                    field="limit", msg="limit query parameter must be greater then zero"
                )

            elif max_limit and max_limit < limit:
                raise create_query_validation_exception(
                    field="limit",
                    msg=f"limit query parameter must be less then {max_limit}",
                )

        return {"skip": skip, "limit": limit}

    return Depends(pagination)
