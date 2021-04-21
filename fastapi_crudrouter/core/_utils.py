from typing import Optional, Type, TypeVar, Any

from fastapi import Depends, HTTPException
from pydantic import create_model

from core._types import PAGINATION, PYDANTIC_SCHEMA

T = TypeVar("T", bound=PYDANTIC_SCHEMA)
FILTER_TYPES = [int, float, bool, str]


def get_pk_type(schema: Type[PYDANTIC_SCHEMA], pk_field: str) -> Any:
    try:
        return schema.__fields__[pk_field].type_
    except KeyError:
        return int


def schema_factory(
    schema_cls: Type[T], pk_field_name: str = "id", name: str = "Create"
) -> Type[T]:
    """
    Is used to create a CreateSchema which does not contain pk
    """

    fields = {
        f.name: (f.type_, ...)
        for f in schema_cls.__fields__.values()
        if f.name != pk_field_name
    }

    name = schema_cls.__name__ + name
    schema = create_model(__model_name=name, **fields)  # type: ignore
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


def query_factory(schema: Type[T]) -> Any:
    field_names = schema.__fields__.keys()

    _str = "{}: Optional[{}] = None"
    args_str = ", ".join(
        [
            _str.format(name, field.type_.__name__)
            for name, field in schema.__fields__.items()
            if field.type_ in FILTER_TYPES
        ]
    )

    _str = "{}={}"
    return_str = ", ".join(
        [
            _str.format(name, field.name)
            for name, field in schema.__fields__.items()
            if field.type_ in FILTER_TYPES
        ]
    )

    filter_func_src = f"""
def filter_func({args_str}):
    ret = dict({return_str})
    return {{k:v for k, v in ret.items() if v is not None}}
"""

    exec(filter_func_src, globals(), locals())
    return Depends(locals().get("filter_func"))
