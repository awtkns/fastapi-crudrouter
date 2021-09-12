import fastapi_crudrouter


def test_version():
    assert type(fastapi_crudrouter.__version__) is str
