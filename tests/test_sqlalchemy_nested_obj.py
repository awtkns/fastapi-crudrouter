from typing import TYPE_CHECKING, Callable, List, Optional

from fastapi.testclient import TestClient
from fastapi_crudrouter import SQLAlchemyCRUDRouter
from sqlalchemy import Column, ForeignKey, Integer, String, Table, inspect
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from tests.implementations.sqlalchemy_ import _setup_base_app
from tests import ORMModel

if TYPE_CHECKING:
    typeguard = True
else:
    typeguard = False

HEROES_URL = "/heroes"
TEAMS_URL = "/teams"
SCHOOLS_URL = "/schools"

Base = declarative_base()


hero_school_link = Table(
    "hero_school_link",
    Base.metadata,
    Column("school_id", Integer, ForeignKey("schools.id"), primary_key=True),
    Column("hero_id", Integer, ForeignKey("heroes.id"), primary_key=True),
)


class School(Base):
    """School DTO."""

    __tablename__ = "schools"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    # heroes = relationship("Hero", secondary="hero_school_link", backref="schools")


class Team(Base):
    """Team DTO."""

    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    headquarters = Column(String)
    heroes = relationship("Hero", back_populates="team")


class Hero(Base):
    """Hero DTO."""

    __tablename__ = "heroes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    team_id = Column(Integer, ForeignKey("teams.id"))
    team = relationship("Team", back_populates="heroes")
    schools = relationship("School", secondary="hero_school_link", backref="heroes")


class TeamRead(ORMModel):
    """Team Read View."""

    name: Optional[str] = None
    headquarters: Optional[str] = None


class TeamCreateUpdate(ORMModel):
    """Team Update View."""

    id: Optional[int] = None
    name: Optional[str] = None
    headquarters: Optional[str] = None

    class Meta:
        """Meta info."""

        orm_model = Team


class SchoolRead(ORMModel):
    """School Read View."""

    name: Optional[str] = None


class SchoolCreateUpdate(ORMModel):
    """School Update/Create View."""

    id: Optional[int] = None
    name: Optional[str] = None

    class Meta:
        """Meta info."""

        orm_model = School


class HeroRead(ORMModel):
    """Hero Read View."""

    name: Optional[str] = None
    team_id: Optional[int] = None
    team: Optional[TeamRead] = None
    schools: Optional[List[SchoolRead]] = []


class HeroCreateUpdate(ORMModel):
    """Hero Update View."""

    id: Optional[int] = None
    name: Optional[str] = None
    team_id: Optional[int] = None
    team: Optional[TeamCreateUpdate] = None
    schools: Optional[List[SchoolCreateUpdate]] = []


def hero_app() -> Callable:
    """Fastapi application."""
    app, engine, _, session = _setup_base_app()
    hero_router = SQLAlchemyCRUDRouter(
        db=session,
        schema=HeroRead,
        update_schema=HeroCreateUpdate,
        create_schema=HeroCreateUpdate,
        db_model=Hero,
        prefix=HEROES_URL,
    )
    app.include_router(hero_router)
    team_router = SQLAlchemyCRUDRouter(
        db=session,
        schema=TeamRead,
        update_schema=TeamCreateUpdate,
        db_model=Team,
        prefix=TEAMS_URL,
    )
    app.include_router(team_router)
    school_router = SQLAlchemyCRUDRouter(
        db=session,
        schema=SchoolRead,
        update_schema=SchoolCreateUpdate,
        create_schema=SchoolCreateUpdate,
        db_model=School,
        prefix=SCHOOLS_URL,
    )
    app.include_router(school_router)
    Base.metadata.create_all(bind=engine)
    return app, session


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}


def test_get():
    """Get all and get one."""
    app, get_session = hero_app()
    client = TestClient(app)
    team = Team(name="Avengers", headquarters="Avengers Mansion")
    session = next(get_session())
    session.add(team)
    hero = Hero(name="Bob", team_id=team.id)
    session.add(hero)
    session.commit()
    session.refresh(hero)

    res = client.get(HEROES_URL)
    assert res.status_code == 200
    assert res.json() == [{**HeroRead(**object_as_dict(hero)).dict()}]

    res = client.get(f"/heroes/{hero.id}")
    assert res.status_code == 200
    assert res.json() == HeroRead(**object_as_dict(hero))


def test_insert() -> None:
    """Test basic sqlmodel insert with relationship attribute as object.hero_client

    This just illustrates what we are trying to do with the crudrouter
    from a sqlmodel perspective.
    """
    _, get_session = hero_app()
    session = next(get_session())
    school_obj1 = School(name="Hero Primary School")
    session.add(school_obj1)

    school_obj2 = School(name="Hero High")
    session.add(school_obj2)

    team = dict(name="Avengers", headquarters="Avengers Mansion")
    team_obj = Team(**team)
    session.add(team_obj)

    session.commit()

    session.refresh(team_obj)
    session.refresh(school_obj1)
    session.refresh(school_obj2)

    hero = dict(name="Bob", team=team_obj, schools=[school_obj1, school_obj2])
    hero_obj = Hero(**hero)
    session.add(hero_obj)
    session.commit()
    session.refresh(hero_obj)

    assert hero["name"] == hero_obj.name
    assert hero["team"] == hero_obj.team
    assert hero["schools"] == [school_obj1, school_obj2]


def test_post_one2many_object():
    """Create an object with a one-to-many relation as object."""
    app, _ = hero_app()
    client = TestClient(app)
    team = dict(name="Avengers", headquarters="Avengers Mansion")
    res = client.post(TEAMS_URL, json=team)
    team_return = res.json()
    assert res.status_code == 200, res.json()

    hero = dict(name="Bob", team=team)
    res = client.post("/heroes", json=hero)
    hero_return = res.json()
    assert res.status_code == 200, hero_return
    assert hero_return["team_id"] == team_return["id"]


def test_post_many2many_object() -> None:
    """Create an object with a many2many relation value as object."""
    app, _ = hero_app()
    client = TestClient(app)
    school = dict(name="Hero Primary School")
    res = client.post(SCHOOLS_URL, json=school)
    school1_return = res.json()
    assert res.status_code == 200, school1_return

    school = dict(name="Hero High")
    res = client.post(SCHOOLS_URL, json=school)
    school2_return = res.json()
    assert res.status_code == 200, school2_return

    hero = dict(
        name="Bob",
        schools=[
            {"id": school1_return["id"]},
            {"id": school2_return["id"]},
        ],
    )

    res = client.post("/heroes", json=hero)
    hero_return = res.json()
    assert res.status_code == 200, hero_return
    assert hero_return["schools"] == [school1_return, school2_return]


def test_update_one2many_object():
    """Update an object with a one-to-many relation as object."""
    app, _ = hero_app()
    client = TestClient(app)
    team = dict(name="Avengers", headquarters="Avengers Mansion")
    res = client.post(TEAMS_URL, json=team)
    team_return = res.json()
    assert res.status_code == 200, res.json()

    hero = dict(name="Bob")
    res = client.post("/heroes", json=hero)
    hero_return = res.json()
    assert res.status_code == 200, hero_return
    assert hero_return["team_id"] is None

    hero_update = dict(team={"name": team_return["name"]})
    res = client.put(f"/heroes/{team_return['id']}", json=hero_update)
    hero_return = res.json()
    assert res.status_code == 200, hero_return
    assert hero_return["team_id"] == team_return["id"]


def test_update_many2many_object() -> None:
    """Create an object and update a many2man relation value as object."""
    app, _ = hero_app()
    client = TestClient(app)
    school1 = dict(name="Hero Primary School")
    res = client.post(SCHOOLS_URL, json=school1)
    school1_return = res.json()
    assert res.status_code == 200, school1_return

    school2 = dict(name="Hero High")
    res = client.post(SCHOOLS_URL, json=school2)
    school2_return = res.json()
    assert res.status_code == 200, school2_return

    hero = dict(name="Bob")
    res = client.post("/heroes", json=hero)
    hero_return = res.json()
    assert res.status_code == 200, hero_return
    assert hero_return["schools"] == []

    hero_update = dict(
        schools=[
            {"id": school1_return["id"]},
            {"id": school2_return["id"]},
        ]
    )
    res = client.put(f"/heroes/{hero_return['id']}", json=hero_update)
    hero_return = res.json()
    assert res.status_code == 200, hero_return
    assert hero_return["schools"] == [school1_return, school2_return]
