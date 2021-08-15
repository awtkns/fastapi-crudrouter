import os
import pathlib


ENV_FILE_PATH = pathlib.Path(__file__).parent / "dev.env"
assert ENV_FILE_PATH.exists()


class BaseConfig:
    POSTGRES_HOST = ""
    POSTGRES_USER = ""
    POSTGRES_PASSWORD = ""
    POSTGRES_DB = ""
    POSTGRES_PORT = ""

    MSSQL_PORT = ""
    SA_PASSWORD = ""

    def __init__(self):
        self._apply_dot_env()
        self._apply_env_vars()
        self.POSTGRES_URI = f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        self.MSSQL_URI = f"mssql+pyodbc://sa:{self.SA_PASSWORD}@{self.POSTGRES_HOST}:{self.MSSQL_PORT}/test?driver=SQL+Server"

    def _apply_dot_env(self):
        with open(ENV_FILE_PATH) as fp:
            for line in fp.readlines():
                line = line.strip(" \n")

                if line and not line.startswith("#"):
                    k, v = line.split("=", 1)

                    if hasattr(self, k) and not getattr(self, k):
                        setattr(self, k, v)

    def _apply_env_vars(self):
        for k, v in os.environ.items():
            if hasattr(self, k):
                setattr(self, k, v)
