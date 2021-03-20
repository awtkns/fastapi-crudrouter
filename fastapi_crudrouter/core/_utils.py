from typing import Callable

from fastapi import HTTPException, Depends
from pydantic import BaseModel, create_model


def get_pk_type(schema, pk_field) -> type:
    try:
        return schema.__fields__[pk_field].type_
    except KeyError:
        return int


def schema_factory(schema_cls: BaseModel, pk_field_name: str = 'id', name: str = 'Create') -> BaseModel:
    """
    Is used to create a CreateSchema which does not contain pk
    """

    fields = {f.name: (f.type_, ...) for f in schema_cls.__fields__.values() if f.name != pk_field_name}

    name = schema_cls.__name__ + name
    schema = create_model(name, **fields)
    return schema


def create_query_validation_exception(field: str, msg: str) -> HTTPException:
    return HTTPException(
        422,
        detail={
            "detail": [{
                "loc": ["query", field],
                "msg": msg,
                "type": "type_error.integer"
            }]
        }
    )


def pagination_factory(max_limit: int = None) -> Callable:
    """
    Created the pagination dependency to be used in the router
    """

    def pagination(skip: int = 0, limit: int = max_limit):
        if skip < 0:
            raise create_query_validation_exception(
                field='skip',
                msg="skip query parameter must be greater or equal to zero"
            )

        if limit is not None:
            if limit <= 0:
                raise create_query_validation_exception(
                    field='limit',
                    msg="limit query parameter must be greater then zero"
                )

            elif max_limit and max_limit < limit:
                raise create_query_validation_exception(
                    field='limit',
                    msg=f"limit query parameter must be less then {max_limit}"
                )

        return {"skip": skip, "limit": limit}

    return Depends(pagination)
