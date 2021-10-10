import os

from sqlalchemy import create_engine
from sqlalchemy.engine.url import make_url
from sqlalchemy_utils import create_database, database_exists, drop_database


class Datasource:
    def __init__(self, name: str, uri: str):
        self.name = name
        self.uri = uri

    def clean(self):
        if database_exists(self.uri):
            drop_database(self.uri)

        create_database(self.uri)


class MssqlDatasource(Datasource):
    def clean(self):
        url = make_url(self.uri)

        db_name = make_url(self.uri).database
        url.database = "master"

        engine = create_engine(url, connect_args={"autocommit": True})
        engine.execute(f"DROP DATABASE IF EXISTS {db_name}")
        engine.execute(f"CREATE DATABASE {db_name}")


class AIOSqlite(Datasource):
    def __init__(self, name: str, uri: str):
        super(AIOSqlite, self).__init__(name=name, uri=uri.lstrip("aio"))

    def clean(self):
        [
            os.remove(f"./db.sqlite3{s}")
            for s in ["", "-wal", "-shm"]
            if os.path.exists(f"./db.sqlite3{s}")
        ]


class StubDataSource(Datasource):
    def clean(self):
        pass


class DatasourceFactory:
    _datasource_map = {}

    def get_datasource(self, uri) -> Datasource:
        name = uri.split(":")[0].split("+")[0].lower()

        return self._datasource_map.get(name, Datasource)(name, uri)

    def register(self, name, cls):
        self._datasource_map[name] = cls


datasource_factory = DatasourceFactory()
datasource_factory.register("mssql", MssqlDatasource)
datasource_factory.register("memory", StubDataSource)
datasource_factory.register("aiosqlite", AIOSqlite)
