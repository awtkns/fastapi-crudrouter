import pytest

from tests import config
from tests.conf.datasource import Datasource, MssqlDatasource, datasource_factory


@pytest.fixture(params=[config.POSTGRES_URI, config.MSSQL_URI])
def datasource(request):
    yield datasource_factory.get_datasource(request.param)


def test_datasource_factory():
    source = datasource_factory.get_datasource(config.POSTGRES_URI)
    assert type(source) is Datasource


def test_datasource_factory_mssql():
    source = datasource_factory.get_datasource(config.MSSQL_URI)
    assert type(source) is MssqlDatasource


def test_clean(datasource: Datasource):
    datasource.clean()
