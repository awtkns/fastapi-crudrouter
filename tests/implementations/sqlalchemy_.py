from sqlalchemy import Column, Float, Integer, String
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from fastapi_crudrouter import SQLAlchemyCRUDRouter
from tests import (
    Carrot,
    CarrotCreate,
    CarrotUpdate,
    CustomPotato,
    PAGINATION_SIZE,
    Potato,
    PotatoType,
    CUSTOM_TAGS,
)
from tests.conf import config
from tests.implementations._base import BaseImpl


class PotatoModel:
    __tablename__ = "potatoes"
    id = Column(Integer, primary_key=True, index=True)
    thickness = Column(Float)
    mass = Column(Float)
    color = Column(String)
    type = Column(String)


class PotatoTypeModel:
    __tablename__ = "potato_type"
    name = Column(String, primary_key=True, index=True)
    origin = Column(String)


class CarrotModel:
    __tablename__ = "carrots"
    id = Column(Integer, primary_key=True, index=True)
    length = Column(Float)
    color = Column(String)


def register_cls(cls, base, to_remove=None, **attrs):
    if to_remove is None:
        to_remove = []

    cls_dict = dict(cls.__dict__)
    cls_dict.update(**attrs)

    new_dict = {
        k: v
        for k, v in cls_dict.items()
        if (not k.startswith("__") or k.startswith("__tablename__"))
        and k not in to_remove
    }

    ext_cls = type(cls.__name__, cls.__bases__, new_dict)

    class Table(ext_cls, base):
        __name__ = ext_cls.__name__

    return Table


class SqlAlchemyImpl(BaseImpl):
    __router__ = SQLAlchemyCRUDRouter
    __backends__ = [config.SQLITE_URI, config.MSSQL_URI, config.POSTGRES_URI]

    def _setup(self):
        engine = create_engine(self.uri, poolclass=NullPool)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        base_cls = declarative_base()

        def session():
            session = SessionLocal()
            try:
                yield session
                session.commit()
            finally:
                session.close()

        return engine, base_cls, session

    def default_impl(self):
        engine, base_cls, session = self._setup()
        potato = register_cls(PotatoModel, base_cls)
        carrot = register_cls(CarrotModel, base_cls)
        base_cls.metadata.create_all(bind=engine)

        return [
            dict(
                schema=Potato,
                db_model=potato,
                db=session,
                prefix="potato",
                paginate=PAGINATION_SIZE,
            ),
            dict(
                schema=Carrot,
                db_model=carrot,
                db=session,
                create_schema=CarrotCreate,
                update_schema=CarrotUpdate,
                prefix="carrot",
                tags=CUSTOM_TAGS,
            ),
        ]

    def custom_ids_impl(self):
        engine, base_cls, session = self._setup()
        custom_ids = register_cls(
            PotatoModel,
            base_cls,
            to_remove=["id"],
            potato_id=Column(Integer, primary_key=True, index=True),
        )

        base_cls.metadata.create_all(bind=engine)

        return [dict(schema=CustomPotato, db_model=custom_ids, db=session)]

    def string_pk_impl(self):
        engine, base_cls, session = self._setup()
        register_cls(PotatoTypeModel, base_cls)
        base_cls.metadata.create_all(bind=engine)

        return [
            dict(
                schema=PotatoType,
                create_schema=PotatoType,
                db_model=PotatoTypeModel,
                db=session,
                prefix="potato_type",
            )
        ]

    def integrity_errors_impl(self):
        engine, base_cls, session = self._setup()
        err_model = register_cls(
            PotatoModel, base_cls, color=Column(String, unique=True)
        )
        base_cls.metadata.create_all(bind=engine)

        return [
            dict(
                schema=Potato,
                db_model=err_model,
                db=session,
                create_schema=Potato,
                prefix="potatoes",
            )
        ]
