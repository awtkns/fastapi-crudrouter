Release Notes
===

## [v0.8.5 - Typing](https://github.com/awtkns/fastapi-crudrouter/releases/tag/v0.8.5) { .releases } 
2022-01-27
### 🎉 Highlights
With the release of v0.8.5 fastapi-crudrouter now officially supports both **Python 3.10** and **typed python**. This release also includes significant improvements to the documentation, test suite, and developer experience. 

Keep an eye of for the next release which will contain support for **async SQLAlchemy** ([#122](https://github.com/awtkns/fastapi-crudrouter/pull/122)). 

Big thanks to all contributors that made this possible!

### ✨ Features
- Typed python support [#132](https://github.com/awtkns/fastapi-crudrouter/pull/132) [#111](https://github.com/awtkns/fastapi-crudrouter/pull/111)
- Python 3.10 support [#114](https://github.com/awtkns/fastapi-crudrouter/pull/114)
- Test suite now runs against multiple databases [#86](https://github.com/awtkns/fastapi-crudrouter/pull/86)
- Documentation improvements [#79](https://github.com/awtkns/fastapi-crudrouter/pull/79) [#91](https://github.com/awtkns/fastapi-crudrouter/pull/91) [#117](https://github.com/awtkns/fastapi-crudrouter/pull/117) [#123](https://github.com/awtkns/fastapi-crudrouter/pull/123) [#124](https://github.com/awtkns/fastapi-crudrouter/pull/124) [#125](https://github.com/awtkns/fastapi-crudrouter/pull/125) [@andrewthetechie](https://github.com/andrewthetechie)
- More informative exceptions [#94](https://github.com/awtkns/fastapi-crudrouter/pull/94) [#137](https://github.com/awtkns/fastapi-crudrouter/pull/137)
- General test suite improvements [#96](https://github.com/awtkns/fastapi-crudrouter/pull/96) [#97](https://github.com/awtkns/fastapi-crudrouter/pull/97)

### 🐛 Bug Fixes
- OrderBy not working correctly with Microsoft SQL Server [#88](https://github.com/awtkns/fastapi-crudrouter/pull/88)
- 404 response not documented in OpenAPI spec [#104](https://github.com/awtkns/fastapi-crudrouter/pull/104) [@sondrelg](https://github.com/sondrelg)
- DatabasesCRUDRouter not functioning for inserts and deletes with AsyncPG [#98](https://github.com/awtkns/fastapi-crudrouter/pull/98)

**Full Changelog**: [`v0.8.0...v0.8.5`](https://github.com/awtkns/fastapi-crudrouter/compare/v0.8.0...v0.8.5)

---

## [v0.8.0 - Gino Backend](https://github.com/awtkns/fastapi-crudrouter/releases/tag/v0.8.0) { .releases } 
2021-07-06
### 🎉 Highlights
With the release of v0.6.0  fastapi-crudrouter **now supports [Gino](https://github.com/python-gino/gino)** as an async backend! When generating routes, GinoCRUDRouter will automatically tie into your database using your Gino models. To use it, simply pass your Gino database model, a database reference, and your pydantic.

```python
GinoCRUDRouter(
    schema=MyPydanticModel,
    db_model=MyModel, 
    db=db
)
```

Check out the [docs](https://fastapi-crudrouter.awtkns.com/backends/gino.html) for more details on how to use the GinoCRUDRouter.

### ✨ Features
- Full Gino Support [@Turall](https://github.com/Turall) [#78](https://github.com/awtkns/fastapi-crudrouter/pull/78) 
- Documentation improvements [#69](https://github.com/awtkns/fastapi-crudrouter/pull/69) [#75](https://github.com/awtkns/fastapi-crudrouter/pull/75) 

### 🐛 Bug Fixes
- All Path Prefixes are now correctly lowercase [#64](https://github.com/awtkns/fastapi-crudrouter/pull/64) [#65](https://github.com/awtkns/fastapi-crudrouter/pull/65)  


---

## [v0.7.0 - Advanced Dependencies ](https://github.com/awtkns/fastapi-crudrouter/releases/tag/v0.7.0) { .releases } 
2021-04-18
### 🎉 Highlights
With the release of v0.7.0 fastapi-crudrouter now provides the ability to set custom dependencies on a per route basis; a much requested feature. Prior to this release, it was only possible to set dependencies for all the routes at once. 

```python
MemoryCRUDRouter(
    schema=MySchema,
    create_route=[Depends(user)],
    delete_all_route=[Depends(admin)]
)
```

Shown above is a brief example on how limiting each route to specific access rights would work using this new feature. Check out the [docs](https://fastapi-crudrouter.awtkns.com/dependencies/) for more details.

### ✨ Features
- Custom Dependencies Per Route [#37](https://github.com/awtkns/fastapi-crudrouter/pull/37) [#59](https://github.com/awtkns/fastapi-crudrouter/pull/59) [#60](https://github.com/awtkns/fastapi-crudrouter/pull/60) [@DorskFR](https://github.com/DorskFR) [@jm-moreau](https://github.com/jm-moreau) 
- Ability to Provide a List of Custom Tags for OpenAPI [#57](https://github.com/awtkns/fastapi-crudrouter/pull/57) [@jm-moreau](https://github.com/jm-moreau) 
- Improved Documentation [#52](https://github.com/awtkns/fastapi-crudrouter/pull/52) 
- Dark Mode for Documentation

---

## [v0.6.0 - Ormar Backend](https://github.com/awtkns/fastapi-crudrouter/releases/tag/v0.6.0) { .releases } 
2021-03-26
### 🎉 Highlights
With the release of v0.6.0  fastapi-crudrouter **now supports [ormar](https://github.com/collerek/ormar)** as an async backend! When generating routes, the OrmarCRUDRouter will automatically tie into your database using your ormar models. To use it, simply pass your ormar database model as the schema.

```python
OrmarCRUDRouter(
    schema=MyPydanticModel, 
    paginate=25
)
```

Check out the [docs](https://fastapi-crudrouter.awtkns.com/backends/ormar/) for more details on how to use the `OrmarCRUDRouter`.

### ✨ Features
- Full Ormar Support [@collerek](https://github.com/collerek) [#46](https://github.com/awtkns/fastapi-crudrouter/pull/46)
- Better handling of database errors in the update route [@sorXCode](https://github.com/sorXCode) [#48](https://github.com/awtkns/fastapi-crudrouter/pull/48) 
- Improved typing [#46](https://github.com/awtkns/fastapi-crudrouter/pull/46) [#43](https://github.com/awtkns/fastapi-crudrouter/pull/43)
- Black, Flake8 and Mypy linting [#46](https://github.com/awtkns/fastapi-crudrouter/pull/46) 
- Additional Tests for nested models [#40](https://github.com/awtkns/fastapi-crudrouter/pull/40) 

### 🐛 Bug Fixes
- Pagination issues when max limit was set to null [@ethanhaid](https://github.com/ethanhaid) [#42](https://github.com/awtkns/fastapi-crudrouter/pull/42) 

---

## [v0.5.0 - Pagination](https://github.com/awtkns/fastapi-crudrouter/releases/tag/v0.5.0) { .releases } 
2021-03-07
### 🎉 Highlights
With the release of v0.5.0 all CRUDRouters  **now supports pagination**. All "get all" routes now accept `skip` and `limit` query parameters allowing you to easily paginate your routes.  By default, no limit is set on the number of items returned by your routes.  Should you wish to limit the number of items that a client can request, it can be done as shown below.

```python
CRUDRouter(
    schema=MyPydanticModel, 
    paginate=25
)
```

Check out the [docs](https://fastapi-crudrouter.awtkns.com/pagination/) on pagination for more information!

### ✨ Features
- Pagination Support [#34](https://github.com/awtkns/fastapi-crudrouter/pull/34) 
- Ability to set custom update schemas [@andreipopovici](https://github.com/andreipopovici) [#31](https://github.com/awtkns/fastapi-crudrouter/pull/31) [#27](https://github.com/awtkns/fastapi-crudrouter/pull/27) 
- Better documentation of past releases [#36](https://github.com/awtkns/fastapi-crudrouter/pull/36)

### 🐛 Bug Fixes
- Prefixing not available for versions of fastapi below v0.62.0 [#29](https://github.com/awtkns/fastapi-crudrouter/pull/29) [#30](https://github.com/awtkns/fastapi-crudrouter/pull/30) 
- Fixed an Import Issue SQLAlchemy and Integrity Errors [@andreipopovici](https://github.com/andreipopovici)  [#33](https://github.com/awtkns/fastapi-crudrouter/pull/33)

---

## [v0.4.0 - Tortoise ORM Support](https://github.com/awtkns/fastapi-crudrouter/releases/tag/v0.4.0) { .releases } 
2021-02-02
### ✨Features
- Full support for tortoise-orm [#24](https://github.com/awtkns/fastapi-crudrouter/pull/24)
- Dynamic pk/id types for get_one, delete_one, and update_one routes [#26](https://github.com/awtkns/fastapi-crudrouter/pull/26)

### 🐛 Bug Fixes  
- Fixed the summary  for the delete one route [#16](https://github.com/awtkns/fastapi-crudrouter/pull/16) 
- Fixed import errors when certain packages are not installed [#21](https://github.com/awtkns/fastapi-crudrouter/pull/21) 
- Improved SQLA type hinting 

---

## [v0.3.0 - Initial Release](https://github.com/awtkns/fastapi-crudrouter/releases/tag/v0.3.0) { .releases } 
2021-01-04
<p align="center">
  <img src="https://raw.githubusercontent.com/awtkns/fastapi-crudrouter/master/docs/en/docs/assets/logo.png" height="200" />
</p>
<h1 align="center">
🎉 Initial Release 🎉
</h1>

Tired of rewriting the same generic CRUD routes? Need to rapidly prototype a feature for a presentation or a hackathon? Thankfully, fastapi-crudrouter has your back. As an extension to the APIRouter included with FastAPI, the FastAPI CRUDRouter will automatically generate and document your CRUD routes for you.

**Documentation**: <a href="https://fastapi-crudrouter.awtkns.com" target="_blank">https://fastapi-crudrouter.awtkns.com</a>

**Source Code**: <a href="https://github.com/awtkns/fastapi-crudrouter" target="_blank">https://github.com/awtkns/fastapi-crudrouter</a>


### Installation
```python
pip install fastapi_crudrouter
``` 

### Usage
Below is a simple example of what the CRUDRouter can do. In just ten lines of code, you can generate all the crud routes you need for any model. A full list of the routes generated can be found here.
```python
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi_crudrouter import MemoryCRUDRouter as CRUDRouter

class Potato(BaseModel):
    id: int
    color: str
    mass: float

app = FastAPI()
app.include_router(CRUDRouter(model=Potato))
```

### Features
- Automatic pydantic model based route generation and documentation ([Docs](https://fastapi-crudrouter.awtkns.com/routing/))
- Ability to customize any of the generated routes ([Docs](https://fastapi-crudrouter.awtkns.com/routing/#overriding-routes))
- Authorization and FastAPI dependency support ([Docs](https://fastapi-crudrouter.awtkns.com/dependencies/))
- Support for both async and non-async relational databases using SQLAlchemy ([Docs](https://fastapi-crudrouter.awtkns.com/backends/sqlalchemy/)) 
- Extensive documentation.
- And much more 😎