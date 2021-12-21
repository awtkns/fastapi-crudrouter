from .conf import BaseConfig


def test__get_sql_server_driver():
    assert "SQL+Server" in BaseConfig._get_sql_server_driver()
