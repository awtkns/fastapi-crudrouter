import os
import pathlib


ENV_FILE_PATH = pathlib.Path(__file__).parent / "dev.env"
assert ENV_FILE_PATH.exists()


class BaseConfig:
    POSTGRES_HOST = "postgres"
    POSTGRES_USER = ""
    POSTGRES_PASSWORD = ""
    POSTGRES_DB = ""

    def __init__(self):
        self._apply_dot_env()
        self._apply_env_vars()
        self.POSTGRES_URI = f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}/{self.POSTGRES_DB}"
        print(self.POSTGRES_URI)

    def _apply_dot_env(self):
        with open(ENV_FILE_PATH) as fp:
            for line in fp.readlines():
                line = line.strip(" \n")

                if not line.startswith("#"):
                    k, v = line.split("=", 1)

                    if hasattr(self, k) and not getattr(self, k):
                        setattr(self, k, v)

    def _apply_env_vars(self):
        for k, v in os.environ.items():
            if hasattr(self, k):
                setattr(self, k, v)
